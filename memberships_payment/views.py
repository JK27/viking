from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import SubscriptionForm
from .models import Subscription, SubscriptionLineItem

from memberships.models import Membership
from membershipsbag.contexts import membershipsbag_contents

import stripe
import json


# --------------------------------------------------------- CACHE PAYMENT DATA
@require_POST
def cache_payment_data(request):
    try:
        # pid is PaymentIntent id
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'membershipsbag': json.dumps(request.session.get('membershipsbag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


# --------------------------------------------------------- PAYMENT
def payment(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        membershipsbag = request.session.get('membershipsbag', {})

        form_data = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        subscription_form = SubscriptionForm(form_data)
        if subscription_form.is_valid():
            # Commit=False prevents multiple save events
            subscription = subscription_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            subscription.stripe_pid = pid
            subscription.original_membershipsbag = json.dumps(membershipsbag)
            subscription.save()
            for item_id, quantity in membershipsbag.items():
                try:
                    membership = Membership.objects.get(id=item_id)
                    subscription_line_item = SubscriptionLineItem(
                        subscription=subscription,
                        membership=membership,
                        quantity=quantity,
                    )
                    subscription_line_item.save()
                # In unlikely event that membership doesn't exist...
                except Membership.DoesNotExist:
                    # ... show error message
                    messages.error(request, (
                        "That membership wasn't found. \
                        Please call us for assistance!")
                    )
                    # ... delete the subscription ...
                    subscription.delete()
                    # ... and redirect user to memberships bag.
                    return redirect(reverse('view_membershipsbag'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('payment_success',
                                    args=[subscription.subscription_number]))
        # If form is not valid, display error message
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')

    else:
        membershipsbag = request.session.get('membershipsbag', {})
        if not membershipsbag:
            messages.error(request,
                           "You haven't selected any memberships.")
            return redirect(reverse('memberships'))

        current_membershipsbag = membershipsbag_contents(request)
        membership_total = current_membershipsbag['membership_total']
        # Stripe total needs to be in £pence
        stripe_total = round(membership_total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        subscription_form = SubscriptionForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'memberships_payment/payment.html'
    context = {
        'subscription_form': subscription_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


# --------------------------------------------------------- PAYMENT SUCCESS
def payment_success(request, subscription_number):
    """
    Handle successful payments
    """

    # save_info = request.session.get('save_info')
    subscription = get_object_or_404(Subscription,
                                     subscription_number=subscription_number)

    messages.success(request, f'Your membership has been successfully processed! \
        Your membership number is {subscription_number}. A confirmation \
        email will be sent to {subscription.email}.')

    # Delete shopping bag from the session as it is no longer needed
    if 'membershipsbag' in request.session:
        del request.session['membershipsbag']

    template = 'memberships_payment/payment_success.html'
    context = {
        'subscription': subscription,
    }

    return render(request, template, context)
