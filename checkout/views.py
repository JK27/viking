from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import OrderLineItem, Order

from shop.models import Product
from profiles.models import UserProfile

from shoppingbag.contexts import shoppingbag_contents

import stripe
import json


# --------------------------------------------------------- CACHE CHECKOUT DATA
@require_POST
def cache_checkout_data(request):
    try:
        # pid is PaymentIntent id
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'shoppingbag': json.dumps(request.session.get('shoppingbag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


# --------------------------------------------------------- CHECKOUT
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        shoppingbag = request.session.get('shoppingbag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            # Commit=False prevents multiple save events
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_shoppingbag = json.dumps(shoppingbag)
            order.save()
            # Iterate through each shopping bag item to create a line item
            for item_id, item_data in shoppingbag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    # If item doesn't have sizes...
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            # ... quantity will just be the item data
                            quantity=item_data,
                        )
                        order_line_item.save()
                    # If item has sizes...
                    else:
                        # ... for each item by size ...
                        for size, quantity in item_data['items_by_size'].items():
                            # ... create a line item
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
                # In unlikely event that product doesn't exist...
                except Product.DoesNotExist:
                    # ... show error message...
                    messages.error(request, (
                        "One of the products in your shopping bag wasn't found. \
                        Please call us for assistance!")
                    )
                    # ... delete the order ...
                    order.delete()
                    # ... and redirect user to shopping bag.
                    return redirect(reverse('view_shoppingbag'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success',
                                    args=[order.order_number]))
        # If form is not valid, display error message
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')

    else:
        shoppingbag = request.session.get('shoppingbag', {})
        if not shoppingbag:
            messages.error(request,
                           "There's nothing in your shopping bag at the moment")
            return redirect(reverse('shop'))

        current_shoppingbag = shoppingbag_contents(request)
        grand_total = current_shoppingbag['grand_total']
        # Stripe total needs to be in £pence
        stripe_total = round(grand_total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


# --------------------------------------------------------- CHECKOUT SUCCESS
def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    #   save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    # ... then display success message
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    # Delete shopping bag from the session as it is no longer needed
    if 'shoppingbag' in request.session:
        del request.session['shoppingbag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
