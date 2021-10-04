from django.contrib import admin
from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
