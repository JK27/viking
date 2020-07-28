from django.shortcuts import render

from .models import Membership, Category, UserMembership


# ------------------------------------------ GET USER MEMBERSHIP
def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None


# ------------------------------------------ MEMBERSHIPS LIST
def list_memberships(request, category_slug=None):
    memberships = Membership.objects.all()
    categories = None
    current_membership = get_user_membership(request)

    if 'category' in request.GET:
        categories = request.GET['category'].split(',')
        memberships = memberships.filter(category__name__in=categories)
        categories = Category.objects.filter(name__in=categories)

    context = {
        "memberships": memberships,
        'current_categories': categories,
        'current_membership': str(current_membership.membership)
    }

    return render(request, "memberships/memberships.html", context)
