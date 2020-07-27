from django.shortcuts import render

from .models import Membership


def list_memberships(request, category_slug=None):
    memberships = Membership.objects.all()

    context = {"memberships": memberships}
    return render(request, "memberships/memberships.html", context)
