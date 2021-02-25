from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display=("username","first_name","last_name","email","password")
class ProductAdmin(admin.ModelAdmin):
    list_display=("prod_id","prod_name","prod_image","seller_id","description","amount","post_date","end_date","active")
class BidAdmin(admin.ModelAdmin):
    list_display=("bid_id","product_id","bid_date","min_amount","bid_amt","bidder_id")
class WatchlistAdmin(admin.ModelAdmin):
    list_display=("list_id","prod_id","user_id")
class CommentAdmin(admin.ModelAdmin):
    list_display=("comment_id","commenter_id","message","prod_id","comment_date")

admin.site.register(User, UserAdmin)
admin.site.register(Products,ProductAdmin)
admin.site.register(Comments,CommentAdmin)
admin.site.register(Bids,BidAdmin)
admin.site.register(WatchList,WatchlistAdmin)