from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import MenuForm, EventBookingForm, EventBookingUpdateForm
from django.contrib.admin.views.decorators import staff_member_required
from .models import EventBooking, User, Menu
from django.http import HttpResponseForbidden
from django.contrib import messages
import razorpay
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from django.utils.timezone import make_aware



def Homepage(request):
    menu = Menu.objects.all().order_by('-price')[:4]
    events = EventBooking.objects.all().order_by('event_date')[:3]  # Fetch the latest 3 events
    context = {
        'name': request.user.username,
        'menu': menu,
        'events': events
    }
    return render(request, 'home.html', context)


def menus(request):
    search_query = request.GET.get('search', '') 
    if search_query:
        menu = Menu.objects.filter(name__icontains=search_query) | Menu.objects.filter(description__icontains=search_query)
    else:
        menu = Menu.objects.all() 

    context = {
        'menu': menu,
        'name': request.user.username
    }
    return render(request, 'menus.html', context)

def menu_item(request, menu_item):
    menu = Menu.objects.get(id=menu_item)
    related_menu = Menu.objects.filter(category=menu.category).exclude(id=menu.id)
    context = { 'menu': menu, 'related_menu': related_menu, 'name': request.user.username }
    return render(request, 'menu_item.html', context)

def related_menu_item(request, related_menu_item):
    menu = Menu.objects.get(id=related_menu_item)
    related_menu = Menu.objects.filter(category=menu.category).exclude(id=menu.id)
    context = { 'menu': menu, 'related_menu': related_menu, 'name': request.user.username }
    return render(request, 'menu_item.html', context)


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully! 🎉")
            return redirect('login')  # Redirect after successful signup
        else:
            # Show form errors as messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    else:
        form = UserRegistrationForm()

    return render(request, "auth/register.html", {"form": form})


def logout_view(request):
    logout(request.user)
    return redirect('homepage')

def verify_razorpay_payment(request, event_id):
    event = get_object_or_404(EventBooking, id=event_id)
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')

    # Initialize Razorpay client
    client = razorpay.Client(auth=("your_razorpay_key_id", "your_razorpay_key_secret"))

    # Verify payment
    payment = client.payment.fetch(payment_id)
    if payment['status'] == 'captured':
        event.payment_status = 'completed'
        event.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed'})



def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, "auth/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('login')





@login_required
def book_event(request):
    booked_dates = list(EventBooking.objects.values_list('event_date', flat=True))

    if request.method == "POST":
        form = EventBookingForm(request.POST)

        event_date_str = request.POST.get("event_date")
        event_date_obj = datetime.strptime(event_date_str, "%Y-%m-%dT%H:%M")  # Convert string to datetime object
        event_date_obj = make_aware(event_date_obj)  # Convert to timezone-aware datetime

        if EventBooking.objects.filter(event_date__date=event_date_obj.date()).exists():
            messages.error(request, "This date is already booked. Please choose another date.")
            return redirect('book_event')

        if form.is_valid():
            event = form.save(commit=False)  # Save the instance first
            event.customer = request.user  # Assign the logged-in user
            event.save()  # Save the event before adding menu items
            form.save_m2m()  # Save ManyToMany field (menu_items)
            return redirect('event_list')  # Redirect to success page
        else:
            return render(request, 'event_booking.html', {'form': form, 'name': request.user.username, 'booked_dates': booked_dates})        
    else:
        form = EventBookingForm()

    return render(request, 'event_booking.html', {'form': form, 'name': request.user.username, 'booked_dates': booked_dates})


@login_required
def event_list(request):
    events = EventBooking.objects.filter(customer=request.user)
    return render(request, 'event_list.html', {'events': events, 'name': request.user.username})


from django.shortcuts import render, redirect
from .models import EventBooking

def cancel_event(request, event_id):

    event = EventBooking.objects.get(id=event_id)

    if event.status != 'completed': 
        event.status = 'cancelled'  
        event.save()

        messages.success(request, "Event has been cancelled successfully.")

    return redirect('event_list')  


def event_details(request, event_id):
    # Fetch the event based on the event_id
    event = get_object_or_404(EventBooking, id=event_id)

    # Render the event details page
    return render(request, 'event_details.html', {'event': event, 'name': request.user.username,})



def update_event(request, event_id):
    event = get_object_or_404(EventBooking, id=event_id)
    
    if request.method == 'POST':
        form = EventBookingUpdateForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('all_events')  # Redirect to the all events page after saving
    else:
        form = EventBookingUpdateForm(instance=event)

    return render(request, 'admin/update_event.html', {'form': form, 'event': event})

@login_required
def dashboard(request):
    user = request.user  # Get the logged-in user
    events = EventBooking.objects.filter(customer=user).order_by('-event_date')  # Fetch user's events
    total_events = events.count()  # Count total events
    upcoming_events = events.filter(event_date__gt=timezone.now()).count()  # Count upcoming events
    past_events = events.filter(event_date__lt=timezone.now()).count()  # Count past events
    total_spent = sum(event.total_price for event in events if event.payment_status == 'completed')  # Sum completed payments

    if not request.user:
        return redirect('login')

    context = {
        'user': user,
        'events': events,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'total_spent': total_spent,
    }
    return render(request, 'dashboard.html', context)


def is_admin(user):
    return user.role == 'admin'



@staff_member_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_menus = Menu.objects.count()
    total_events = EventBooking.objects.count()
    pending_events = EventBooking.objects.filter(status='pending').count()
    approved_events = EventBooking.objects.filter(status='approved').count()
    completed_events = EventBooking.objects.filter(status='completed').count()
    cancelled_events = EventBooking.objects.filter(status='cancelled').count()
    
    total_revenue = sum(event.total_price for event in EventBooking.objects.filter(status="completed"))

    recent_events = EventBooking.objects.order_by('-event_date')[:5]  # Show 5 latest events

    context = {
        'total_users': total_users,
        'total_menus': total_menus,
        'total_events': total_events,
        'pending_events': pending_events,
        'approved_events': approved_events,
        'completed_events': completed_events,
        'cancelled_events': cancelled_events,
        'total_revenue': total_revenue,
        'recent_events': recent_events,
<<<<<<< HEAD
        'name': request.user.username
=======
        'name' : request.user.username
>>>>>>> d0389d6 (one event on single date)
    }
    return render(request, 'admin_dashboard.html', context)

@staff_member_required
def menu_list(request):
    menus = Menu.objects.all()
    return render(request, 'admin/menu_list.html', {'menus': menus, 'name': request.user.username})

@staff_member_required
def add_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuForm()
    return render(request, 'admin/add_menu.html', {'form': form, 'name': request.user.username})

@staff_member_required
def edit_menu(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES, instance=menu)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuForm(instance=menu)
    return render(request, 'admin/edit_menu.html', {'form': form, 'name': request.user.username})

@staff_member_required
def delete_menu(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    menu.delete()
    return redirect('menu_list')



@login_required
def order_menu_view(request):
    menu_items = Menu.objects.all()
    return render(request, "order_menu.html", {"menu_items": menu_items})

@login_required
def place_order_view(request):
    if request.method == "POST":
        items = Menu.objects.filter(id__in=request.POST.getlist('menu_items'))
        total_price = sum(item.price for item in items)
        order = Order.objects.create(customer=request.user, total_price=total_price, status='pending')
        order.items.set(items)
        return redirect('order_confirmation', order_id=order.id)
    menu_items = Menu.objects.all()
    return render(request, "place_order.html", {"menu_items": menu_items})

@login_required
def order_confirmation_view(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, "order_confirmation.html", {"order": order})

@login_required
def order_history_view(request):
    orders = Order.objects.filter(customer=request.user)
    return render(request, "order_history.html", {"orders": orders})




# Razorpay client setup
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def process_payment(request, event_id):
    event = get_object_or_404(EventBooking, id=event_id)

    # Create a Razorpay order
    amount = int(event.total_price * 100)  # Razorpay requires amount in paise
    currency = "INR"
    payment_order = razorpay_client.order.create({
        "amount": amount,
        "currency": currency,
        "payment_capture": "1"
    })

    # Store the Razorpay order ID
    event.razorpay_payment_id = payment_order["id"]
    event.save()

    return JsonResponse({
        "order_id": payment_order["id"],
        "amount": amount,
        "currency": currency,
        "key": settings.RAZORPAY_KEY_ID
    })


@login_required
def verify_razorpay_payment(request, event_id):
    event = get_object_or_404(EventBooking, id=event_id)
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')
    signature = request.GET.get('signature')

    try:
        razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        })
        event.payment_status = 'completed'
        event.status = 'approved'
        event.save()
        return redirect('payment_success')
    except razorpay.errors.SignatureVerificationError:
        event.status = 'pending'
        event.save()
        return redirect('payment_failed')


def payment_success(request, event_id):
    event = get_object_or_404(EventBooking, id=event_id, payment_status='completed')
    return render(request, 'payment_success.html', {'event': event})

def about(request):
    return render(request, 'about.html', {'name': request.user})


def all_events(request):
    events = EventBooking.objects.all().order_by('-event_date')
    return render(request, 'admin/all_events.html', {'events': events})
