from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Menu
from .forms import MenuForm
from django.contrib.admin.views.decorators import staff_member_required
from .models import Menu, Order
from django.http import HttpResponseForbidden

def Homepage(request):
    menu = Menu.objects.all().order_by('-price')[:4]
    context = {
        'name': request.user.username,
        'menu': menu
    }
    return render(request, 'home.html', context)

def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Redirect to login page instead of dashboard
    else:
        form = UserRegistrationForm()
    return render(request, "auth/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserLoginForm()
    return render(request, "auth/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('login')



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
