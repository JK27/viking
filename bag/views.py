from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from shop.models import Product


# ------------------------------------- VIEW BAG
def view_bag(request):
    return render(request, 'bag/bag.html')


# ------------------------------------- ADD TO BAG
def add_to_bag(request, item_id):
    """ Adds quantity of specified product to shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    # Quantity needs conversion to int as comes as string from from
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # Keeps bag contents while session lasts. If not session, it creates one
    bag = request.session.get('bag', {})

    # If product has sizes...
    if size:
        # ... and if product is already in bag...
        if item_id in list(bag.keys()):
            # ... and if it has same size...
            if size in bag[item_id]['items_by_size'].keys():
                # ... then update quantity accordingly...
                bag[item_id]['items_by_size'][size] += quantity
                messages.success(request, f'Updated size {size.upper()} \
                {product.name} quantity to \
                {bag[item_id]["items_by_size"][size]}.')
            # ... but if it has a different size...
            else:
                # ... then add quantity of items of that size ...
                bag[item_id]['items_by_size'][size] = quantity
                # ... and display succes message in toasts
                messages.success(request, f'Added size {size.upper()} \
                {product.name} to your bag.')
        # But if product is not already in bag...
        else:
            # ... adds quantity of items of each size to bag
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added size {size.upper()} \
            {product.name} to your bag.')
    # If product does not have sizes...
    else:
        # ...and if item already exists in bag ...
        if item_id in list(bag.keys()):
            # ...updates quantity accordingly
            bag[item_id] += quantity
            # ... and display succes message in toasts
            messages.success(request, f'Updated {product.name} quantity to \
            {bag[item_id]}.')
        # But if item not alreay in bag ...
        else:
            # ... adds specified quantity of items to bag
            bag[item_id] = quantity
            # ... and display succes message in toasts
            messages.success(request, f'Added {product.name} to your bag.')
    # Overwrites variable in session with updated version
    request.session['bag'] = bag
    return redirect(redirect_url)


# --------------------------------------------------------- ADJUST BAG
def adjust_bag(request, item_id):
    """ Adjusts the quantity of specified product to specified amount """

    product = get_object_or_404(Product, pk=item_id)
    # Quantity needs conversion to int as comes as string from from
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # Keeps bag contents while session lasts. If not session, it creates one
    bag = request.session.get('bag', {})

    # If product has sizes...
    if size:
        # ... and if quantity is greater than 0...
        if quantity > 0:
            # ... sets quantity accordingly...
            bag[item_id]['items_by_size'][size] = quantity
            # ... and display succes message in toasts
            messages.success(request, f'Updated size {size.upper()} \
            {product.name} quantity to {bag[item_id]["items_by_size"][size]}.')

        # ... otherwise...
        else:
            # ... removes the item of that size
            del bag[item_id]['items_by_size'][size]
            # If there is no ohter sizes of the same item in bag...
            if not bag[item_id]['items_by_size']:
                # ... removes item completely
                bag.pop(item_id)
            # ... and display succes message in toasts
            messages.success(request, f'Removed size {size.upper()} \
            {product.name} from your bag.')
    # If product does not have sizes...
    else:
        # ... and if quantity is greater than 0...
        if quantity > 0:
            # ... sets quantity accordingly...
            bag[item_id] = quantity
            # ... and display succes message in toasts
            messages.success(request, f'Updated {product.name} \
                                        quantity to {bag[item_id]}.')
        # ... otherwise...
        else:
            # ... removes the item completely
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag.')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


# --------------------------------------------------------- REMOVE CONTENTS
def remove_from_bag(request, item_id):
    """ Removes item from bag """

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        # Keeps bag contents during session. If not session, it creates one
        bag = request.session.get('bag', {})

        # If product has sizes...
        if size:
            # ... removes the item of that size
            del bag[item_id]['items_by_size'][size]
            # If there is no ohter sizes of the same item in bag...
            if not bag[item_id]['items_by_size']:
                # ... removes item completely
                bag.pop(item_id)
            # ... and display succes message in toasts
            messages.success(request, f'Removed size {size.upper()} \
            {product.name} from your bag.')
        # If product does not have sizes...
        else:
            # ... removes the item completely
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag.')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
