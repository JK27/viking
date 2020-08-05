from django.shortcuts import get_object_or_404
from shop.models import Product


# ------------------------------------- SHOPPING BAG CONTENTS
def shoppingbag_contents(request):

    shoppingbag_items = []      # Empty list for items to live in
    total = 0           # Total amount initiates at 0
    product_count = 0   # Product count initiates at 0
    # Keeps bag contents during session.
    shoppingbag = request.session.get('shoppingbag', {})

    # For each item in the shopping bag...
    for item_id, item_data in shoppingbag.items():
        # If item_data is integer it means it is just quantity with no sizes
        if isinstance(item_data, int):
            # ... first, we get the product ...
            product = get_object_or_404(Product, pk=item_id)
            # ... then add price of all items to the total ...
            total += item_data * product.price
            # ... and number of products to total count
            product_count += item_data

            shoppingbag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        # If item has sizes ...
        else:
            # ... first, we get the product ...
            product = get_object_or_404(Product, pk=item_id)
            # ... then the products for each size ...
            for size, quantity in item_data['items_by_size'].items():
                # ... then add price of all items to the total ...
                total += quantity * product.price
                # ... and number of products to total count
                product_count += quantity

                shoppingbag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })

    grand_total = total

    context = {
        'shoppingbag_items': shoppingbag_items,
        'total': total,
        'product_count': product_count,
        'grand_total': grand_total,
    }

    return context
