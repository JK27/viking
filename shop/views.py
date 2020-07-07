from django.shortcuts import render


# ------------------------------------- ALL PRODUCTS
def all_products(request):
    return render(request, 'shop/includes/shop_nav.html')
