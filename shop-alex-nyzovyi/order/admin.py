from django.contrib import admin

from order.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_paid')
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
