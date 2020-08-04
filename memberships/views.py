from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import Membership, Category, UserMembership, Subscription

import stripe


# ------------------------------------------ GET USER MEMBERSHIP
def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    else:
        return None


# ------------------------------------------ GET USER SUBSCRIPTION
def get_user_subscription(request):
    user_subscription_qs = Subscription.objects.filter(
        user_membership=get_user_membership(request))
    if user_subscription_qs.exists():
        user_subscription = user_subscription_qs.first()
        return user_subscription
    return None


# ------------------------------------------ GET SELECTED MEMBERSHIP
def get_selected_membership(request):
    membership_type = request.session['selected_membership_type']
    selected_membership_qs = Membership.objects.filter(
        membership_type=membership_type)
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None


# ------------------------------------------ MEMBERSHIPS LIST
def list_memberships(request, category_slug=None):
    memberships = Membership.objects.all()
    categories = None

    if request.user.is_authenticated:
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

    else:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            memberships = memberships.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        context = {
            "memberships": memberships,
            'current_categories': categories,
        }

        return render(request, "memberships/memberships.html", context)


# ------------------------------------- MEMBERSHIP DETAIL
def membership_detail(request, membership_id):
    """ Display individual membership details """

    membership = get_object_or_404(Membership, pk=membership_id)

    context = {
        'membership': membership,
    }

    return render(request, 'memberships/membership_detail.html', context)


# ------------------------------------- VIEW SELECTED MEMBERSHIP
def view_selected_membership(request):
    return render(request, 'memberships/view_selected_membership.html')


# ------------------------------------- SELECT MEMBERSHIP
def select_membership(request, item_id):
    """ Selects membership """

    membership = get_object_or_404(Membership, pk=item_id)
    request.session['membership'] = membership
    return render(request, 'memberships/membership_payment.html')








############################################################
# ------------------------------------- SELECT MEMBERSHIP
# def select_membership(request, **kwargs):
#     selected_membership_type = request.POST.get('membership_type')

#     user_membership = get_user_membership(request)
#     user_subscription = get_user_subscription(request)

#     selected_membership_qs = Membership.objects.filter(
#         membership_type=selected_membership_type
#     )

#     if selected_membership_qs.exists():
#         selected_membership = selected_membership_qs.first()

    # Validation
    # if user_membership.membership == selected_membership:
    #     if user_subscription is not None:
    #         messages.info(request, "This is your current membership. Your \
    #                       next payment is due {}".format('get it from stripe'))
            # redirect user to page they are coming from
            # return redirect(request.META.get('HTTP_REFERER'))

    # assign to the session
    # request.session['selected_membership_type'] = selected_membership.membership_type

    # return render(request, 'memberships/membership_payment.html')


# ------------------------------------- PAYMENT
# @login_required
# def membership_payment(request):
#     user_membership = get_user_membership(request)

#     selected_membership = get_selected_membership(request)

#     stripe_public_key = settings.STRIPE_PUBLISHABLE_KEY

#     context = {
#         'stripe_public_key': stripe_public_key,
#         'selected_membership': selected_membership
#     }

#     return render(request, "memberships/membership_payment.html", context)
