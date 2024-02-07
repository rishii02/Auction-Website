from django.contrib import admin
from auctions.models import User,listings,bid,watchlist,comments
# Register your models here.
admin.site.register(User)
admin.site.register(listings)
admin.site.register(bid)
admin.site.register(watchlist)
admin.site.register(comments)