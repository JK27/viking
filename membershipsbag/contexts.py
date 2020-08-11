from django.shortcuts import get_object_or_404
from memberships.models import Membership


# ------------------------------------- MEMBERSHIPS BAG CONTENTS
def membershipsbag_contents(request):
    membershipsbag_items = []      # Empty list for items to live in
    membership_total = 0           # Total amount initiates at 0
    membership_count = 0   # Membership count initiates at 0
    membershipsbag = request.session.get('membershipsbag', {})

    for item_id, quantity in membershipsbag.items():
        membership = get_object_or_404(Membership, pk=item_id)
        membership_total = quantity * membership.price
        membershipsbag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'membership': membership,
        })

    context = {
        'membershipsbag_items': membershipsbag_items,
        'membership_total': membership_total,
        'membership_count': membership_count,
    }

    return context
