from django.shortcuts import render, redirect


# ------------------------------------- VIEW MEMBERSHIPS BAG
def view_membershipsbag(request):
    """ Displays memberships bag contents page. """

    return render(request, 'membershipsbag/membershipsbag.html')


# ------------------------------------- ADD TO MEMBERSHIPS BAG
def add_to_membershipsbag(request, item_id):
    """ Adds selected membership to the bag """

    # Quantity needs conversion to int as comes as string from form
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    membershipsbag = request.session.get('membershipsbag', {})

    membershipsbag[item_id] = quantity

    request.session['membershipsbag'] = membershipsbag
    return redirect(redirect_url)
