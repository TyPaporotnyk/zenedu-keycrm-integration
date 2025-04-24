from django.contrib import admin

from apps.zenedu.models import Bot, Order, Subscriber


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ("name", "username", "is_active", "created_at")
    search_fields = ("name", "username")
    list_filter = ("is_active", "created_at")


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "username", "phone", "created_at")
    search_fields = ("first_name", "last_name", "username", "phone")
    list_filter = ("created_at",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("price", "currency", "status", "payment_system_type", "created_at")
    search_fields = ("first_name", "last_name", "username", "phone")
    list_filter = ("status", "payment_system_type", "created_at")
    list_select_related = ("bot", "subscriber")
