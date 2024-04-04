from django.contrib import admin
from .models import login_info, Item, Poll, Choice, Product, Order, OrderItem, Category, Voucher


# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice


class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


admin.site.register(login_info)
admin.site.register(Item)

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)


class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)

admin.site.register(Voucher)