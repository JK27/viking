from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import SubscriptionForm


# --------------------------------------------------------- PAYMENT
def payment(request):
    membershipsbag = request.session.get('membershipsbag', {})
    if not membershipsbag:
        messages.error(request,
                       "You haven't selected any memberships.")
        return redirect(reverse('memberships'))

    subscription_form = SubscriptionForm()
    template = 'memberships_payment/payment.html'
    context = {
        'subscription_form': subscription_form,
    }

    return render(request, template, context)
