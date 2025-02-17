from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import MenuForm, EventBookingForm
from django.contrib.admin.views.decorators import staff_member_required
from .models import Menu, EventBooking
from django.http import HttpResponseForbidden
from django.contrib import messages
import razorpay
from django.http import JsonResponse






def Homepage(request):
    menu = Menu.objects.all().order_by('-price')[:4]
    search_query = request.GET.get('search', '')  # Get the search query from the URL parameter
    if search_query:
        menu = Menu.objects.filter(name__icontains=search_query) | Menu.objects.filter(description__icontains=search_query)
    else:
        menu = Menu.objects.all() 
    events = EventBooking.objects.all()[:3]  # Fetch the latest 3 events
    context = {
        'name': request.user.username,
        'menu': menu,
        'events': events
    }
    return render(request, 'home.html', context)



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



# Razorpay Client Setup
razorpay_client = razorpay.Client(auth=("RAZORPAY_KEY_ID", "RAZORPAY_KEY_SECRET"))

@login_required
def book_event(request):
    if request.method == "POST":
        form = EventBookingForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)  # Save the instance first
            event.customer = request.user  # Assign the logged-in user
            event.save()  # Save the event before adding menu items
            form.save_m2m()  # Save ManyToMany field (menu_items)
            return redirect('event_list')  # Redirect to success page
    else:
        form = EventBookingForm()

    return render(request, 'event_booking.html', {'form': form})


@login_required
def event_list(request):
    events = EventBooking.objects.filter(customer=request.user)
    return render(request, 'event_list.html', {'events': events})


from django.shortcuts import render, redirect
from .models import EventBooking

def cancel_event(request, event_id):
    # Get the event based on the ID
    event = EventBooking.objects.get(id=event_id)

    # Check if the user is authorized to cancel the event (optional)
    if event.status != 'completed':  # You can also add additional logic here for authorization
        event.status = 'cancelled'  # Update the status to 'cancelled'
        event.save()
        # Optionally, add a success message
        messages.success(request, "Event has been cancelled successfully.")

    return redirect('event_list')  # Redirect back to the event list page


def event_details(request, event_id):
    # Fetch the event based on the event_id
    event = get_object_or_404(EventBooking, id=event_id)

    # Render the event details page
    return render(request, 'event_details.html', {'event': event})


@login_required
def dashboard(request):
    return render(request, "dashboard.html")


def is_admin(user):
    return user.role == 'admin'


# Ensure only admin can access the admin dashboard
@login_required
def admin_dashboard_view(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to view this page.")
    return render(request, 'admin_dashboard.html')


@staff_member_required
def menu_list_view(request):
    menu_items = Menu.objects.all()
    return render(request, "admin/menu_list.html", {"menu_items": menu_items})

@staff_member_required
def add_menu_item_view(request):
    if request.method == "POST":
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuForm()
    return render(request, "admin/add_menu_item.html", {"form": form})

@staff_member_required
def edit_menu_item_view(request, pk):
    menu_item = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        form = MenuForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('menu_list')
    else:
        form = MenuForm(instance=menu_item)
    return render(request, "admin/edit_menu_item.html", {"form": form})

@staff_member_required
def delete_menu_item_view(request, pk):
    menu_item = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        menu_item.delete()
        return redirect('menu_list')
    return render(request, "admin/delete_menu_item.html", {"menu_item": menu_item})




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
