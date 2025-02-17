from django.contrib import admin
from .models import User, Menu, EventBooking

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



@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'customer', 'status', 'total_price')
    list_filter = ('status',)
    actions = ['approve_event']

    def approve_event(self, request, queryset):
        queryset.update(status='approved')
    approve_event.short_description = "Approve selected events"

