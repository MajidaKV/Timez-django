# from .views import _wishlist_id
# from .models import Wishlist, WishlistItem


# def counter(request):
#     wish_counter=0
#     wishlist_itams=None
#     if 'admin' in request.path:
#         return{}
#     else:
#         try:
#             wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
#             wishlist_itams=WishlistItem.objects.filter(wishlist=wishlist, is_active = True),
#             if wishlist_itams!=0:
#                 wish_counter=WishlistItem.objects.filter(wishlist=wishlist, is_active = True).count()
#             else:
#                 wish_counter=0
#         except Wishlist.DoesNotExist:
#             wish_counter=0
#             pass
#     return {
#        'wishlist_itams':WishlistItem.objects.filter(wishlist=wishlist, is_active = True),
#        'wish_counter':wish_counter,
#      }