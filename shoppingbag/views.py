from django.shortcuts import (render, redirect, reverse,
                              HttpResponse, get_object_or_404)
from django.contrib import messages
from shop.models import Product


# ------------------------------------- VIEW SHOPPING BAG
def view_shoppingbag(request):
    """ Displays shopping bag contents page. """
    return render(request, 'shoppingbag/shoppingbag.html')


# ------------------------------------- ADD TO SHOPPING BAG
def add_to_shoppingbag(request, item_id):
    """ Adds quantity of specified product to shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    # Quantity needs conversion to int as comes as string from form
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # Keeps shopping bag contents while session lasts.
    # If not session, it creates one
    shoppingbag = request.session.get('shoppingbag', {})

    # If product has sizes...
    if size:
        # ... and if product is already in bag...
        if item_id in list(shoppingbag.keys()):
            # ... and if it has same size...
            if size in shoppingbag[item_id]['items_by_size'].keys():
                # ... then update quantity accordingly...
                shoppingbag[item_id]['items_by_size'][size] += quantity
                messages.success(request, f'Updated size {size.upper()} \
                {product.name} quantity to \
                {shoppingbag[item_id]["items_by_size"][size]}.')
            # ... but if it has a different size...
            else:
                # ... then add quantity of items of that size ...
                shoppingbag[item_id]['items_by_size'][size] = quantity
                # ... and display succes message in toasts
                messages.success(request, f'Added size {size.upper()} \
                {product.name} to your shopping bag.')
        # But if product is not already in shopping bag...
        else:
            # ... adds quantity of items of each size to shopping bag
            shoppingbag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added size {size.upper()} \
            {product.name} to your shopping bag.')
    # If product does not have sizes...
    else:
        # ...and if item already exists in shopping bag ...
        if item_id in list(shoppingbag.keys()):
            # ...updates quantity accordingly
            shoppingbag[item_id] += quantity
            # ... and display succes message in toasts
            messages.success(request, f'Updated {product.name} quantity to \
            {shoppingbag[item_id]}.')
        # But if item not alreay in shopping bag ...
        else:
            # ... adds specified quantity of items to shopping bag
            shoppingbag[item_id] = quantity
            # ... and display succes message in toasts
            messages.success(request, f'Added {product.name} to your shopping bag.')
    # Overwrites variable in session with updated version
    request.session['shoppingbag'] = shoppingbag
    return redirect(redirect_url)


# --------------------------------------------------------- ADJUST SHOPPING BAG
def adjust_shoppingbag(request, item_id):
    """ Adjusts the quantity of specified product to specified amount """

    product = get_object_or_404(Product, pk=item_id)
    # Quantity needs conversion to int as comes as string from from
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # Keeps shopping bag contents while session lasts. If not session, it creates one
    shoppingbag = request.session.get('shoppingbag', {})

    # If product has sizes...
    if size:
        # ... and if quantity is greater than 0...
        if quantity > 0:
            # ... sets quantity accordingly...
            shoppingbag[item_id]['items_by_size'][size] = quantity
            # ... and display succes message in toasts
            messages.success(request, f'Updated size {size.upper()} \
            {product.name} quantity to {shoppingbag[item_id]["items_by_size"][size]}.')

        # ... otherwise...
        else:
            # ... removes the item of that size
            del shoppingbag[item_id]['items_by_size'][size]
            # If there is no ohter sizes of the same item in shopping bag...
            if not shoppingbag[item_id]['items_by_size']:
                # ... removes item completely
                shoppingbag.pop(item_id)
            # ... and display succes message in toasts
            messages.success(request, f'Removed size {size.upper()} \
            {product.name} from your shopping bag.')
    # If product does not have sizes...
    else:
        # ... and if quantity is greater than 0...
        if quantity > 0:
            # ... sets quantity accordingly...
            shoppingbag[item_id] = quantity
            # ... and display succes message in toasts
            messages.success(request, f'Updated {product.name} \
                                        quantity to {shoppingbag[item_id]}.')
        # ... otherwise...
        else:
            # ... removes the item completely
            shoppingbag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your shopping bag.')

    request.session['shoppingbag'] = shoppingbag
    return redirect(reverse('view_shoppingbag'))


# --------------------------------------------------------- REMOVE CONTENTS
def remove_from_shoppingbag(request, item_id):
    """ Removes item from shopping bag """

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        # Keeps shopping bag contents during session. If not session, it creates one
        shoppingbag = request.session.get('shoppingbag', {})

        # If product has sizes...
        if size:
            # ... removes the item of that size
            del shoppingbag[item_id]['items_by_size'][size]
            # If there is no ohter sizes of the same item in shopping bag...
            if not shoppingbag[item_id]['items_by_size']:
                # ... removes item completely
                shoppingbag.pop(item_id)
            # ... and display succes message in toasts
            messages.success(request, f'Removed size {size.upper()} \
            {product.name} from your shopping bag.')
        # If product does not have sizes...
        else:
            # ... removes the item completely
            shoppingbag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your shopping bag.')

        request.session['shoppingbag'] = shoppingbag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
