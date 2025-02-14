from django.contrib import admin
from .models import User, Menu, Order, EventBooking, Payment

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_price', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('customer__username', 'status')

@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'event_type', 'venue', 'event_date', 'guest_count', 'status')
    list_filter = ('event_type', 'status')
    search_fields = ('customer__username', 'venue')
    ordering = ('-event_date',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'payment_status', 'transaction_id')
    list_filter = ('payment_status',)
    search_fields = ('transaction_id', 'order__customer__username')

