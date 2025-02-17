from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('staff', 'Catering Staff'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    groups = models.ManyToManyField(Group, related_name="catering_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="catering_user_permissions", blank=True)

    def __str__(self):
        return self.username

class Menu(models.Model):
    CATEGORY_CHOICES = [
        ('veg', 'Vegetarian'),
        ('non-veg', 'Non-Vegetarian'),
        ('beverages', 'Beverages'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

class EventBooking(models.Model):
    EVENT_CHOICES = [
        ('wedding', 'Wedding'),
        ('birthday', 'Birthday'),
        ('corporate', 'Corporate Event'),
        ('engagement', 'Engagement'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES, default='other')
    event_date = models.DateTimeField()
    venue = models.CharField(max_length=255)
    guest_count = models.IntegerField()
    menu_items = models.ManyToManyField(Menu)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    razorpay_payment_id = models.CharField(max_length=255, null=True, blank=True)

    def calculate_total_price(self):
        menu_total = sum(item.price for item in self.menu_items.all())
        extra_charges = self.guest_count * 250  
        base_charge = 5000  
        return menu_total + extra_charges + base_charge

    
    def save(self, *args, **kwargs):
        if not self.pk:  # If the instance is not yet saved (no primary key)
            super().save(*args, **kwargs)  # Save it first
        
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)  # Save again after total_price calculation


    def __str__(self):
        return f"{self.get_event_type_display()} on {self.event_date} at {self.venue}"
