from django.shortcuts import get_object_or_404
from shop.models import Product


# ------------------------------------- BAG CONTENTS
def bag_contents(request):

    bag_items = []      # Empty list for items to live in
    total = 0           # Total amount initiates at 0
    product_count = 0   # Product count initiates at 0
    bag = request.session.get('bag', {})  # Keeps bag contents during session.

    # For each item in the bag...
    for item_id, item_data in bag.items():
        # If item_data is integer it means it is just quantity with no sizes
        if isinstance(item_data, int):
            # ... first, we get the product ...
            product = get_object_or_404(Product, pk=item_id)
            # ... then add price of all items to the total ...
            total += item_data * product.price
            # ... and number of products to total count
            product_count += item_data

            bag_items.append({
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

                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })

    grand_total = total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'grand_total': grand_total,
    }

    return context
