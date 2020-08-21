from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm

from memberships_payment.models import Subscription


# --------------------------------------------------------- PROFILE
@login_required
def profile(request):
    """ Display user's profile"""
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated succesfully.')
        else:
            messages.error(request, 'Failed to update your profile. \
                           Please ensure the form is correct.')
    # else:
    form = UserProfileForm(instance=profile)
    subscriptions = profile.subscriptions.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'subscriptions': subscriptions,
        'on_profile_page': True,
    }

    return render(request, template, context)


# --------------------------------------------------------- ORDER HISTORY
def user_subscription(request, subscription_number):
    subscription = get_object_or_404(Subscription,
                                     subscription_number=subscription_number)

    messages.info(request, (
        f'This is a past confirmation for order number {subscription_number}.'
        'A confirmation email was sent on the order date.'
    ))

    template = 'memberships_payment/payment_success.html'
    context = {
        'subscription': subscription,
        'from_profile': True,
    }

    return render(request, template, context)
