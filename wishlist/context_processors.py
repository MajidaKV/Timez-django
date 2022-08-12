from .views import _wishlist_id
from .models import Wishlist, WishlistItem


def counter(request):
    wishlist_count=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            wishlist=Wishlist.objects.filter(_wishlist_id=_wishlist_id(request))
            if request.user.is_authenticated:
                wishlist_items=WishlistItem.objects.all().filter(user=request.user)
            else:
                wishlist_items=WishlistItem.objects.all().filter(wishlist=wishlist[:1])
            for wishlist_item in wishlist_items:
                wishlist_count += wishlist_item.quantity
        except Wishlist.DoesNotExist:
            wishlist_count=0
    return dict(wishlist_count=wishlist_count)