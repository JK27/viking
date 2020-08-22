from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import Membership, Category

import stripe


# ------------------------------------------ MEMBERSHIPS LIST
def list_memberships(request, category_slug=None):
    memberships = Membership.objects.all()
    categories = None

    if request.user.is_authenticated:

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            memberships = memberships.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        context = {
            "memberships": memberships,
            'current_categories': categories,
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
