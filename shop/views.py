from django.shortcuts import render, get_object_or_404
from .models import Product


# ------------------------------------- ALL PRODUCTS
def all_products(request):
    """ Display all products, indlucing sorting and search queries """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'shop/products.html', context)


# ------------------------------------- PRODUCT DETAIL
def product_detail(request, product_id):
    """ Display individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'shop/product_detail.html', context)
