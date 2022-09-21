from django.contrib import admin

from auctions.models import Product, Bid, Remark, User

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "desc", "startBid", "img", "category", "status",]

class BidAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "amount"]

class RemarkAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "message", "time"]

admin.site.register(Product, ProductAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Remark, RemarkAdmin)
admin.site.register(User)