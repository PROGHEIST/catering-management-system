from django.contrib import admin
from .models import User, Menu, EventBooking

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff')
    search_fields = ('username', 'email')

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'image_preview')
    list_filter = ('category',)
    search_fields = ('name', 'category')
    ordering = ('category', 'name')

    def image_preview(self, obj):
        return f'<img src="{obj.image.url}" width="50" height="50"/>'
    image_preview.allow_tags = True
    image_preview.short_description = "Image"


@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'event_type', 'event_date', 'venue', 'guest_count', 'total_price', 'status', 'payment_status')
    list_filter = ('event_type', 'status', 'payment_status')
    search_fields = ('customer__username', 'venue')
    ordering = ('-event_date',)
