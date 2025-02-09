from django.contrib import admin
from .models import User, Menu, Order, EventBooking, Payment

admin.site.register(User)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(EventBooking)
admin.site.register(Payment)
