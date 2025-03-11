from django.shortcuts import render
from django.urls import path
from .views import Homepage, register_view,all_events, login_view, logout_view, update_event,  dashboard,menu_list, add_menu, edit_menu, delete_menu, order_menu_view, place_order_view, order_confirmation_view, order_history_view,book_event, event_list, cancel_event, event_details, menus, menu_item, related_menu_item, process_payment, verify_razorpay_payment, payment_success, about, admin_dashboard
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Homepage, name='home'),
    path('menus/', menus, name='menus'),
    path('menus/<int:menu_item>', menu_item, name='menu-details'),
    path('menus/<int:related_menu_item>', related_menu_item, name='related_menu-details'),
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('book-event/', book_event, name='book_event'),
    path('events/', event_list, name='event_list'),
    path('events/<int:event_id>/', event_details, name='event_details'),
    path('events/<int:event_id>/pay/', process_payment, name='initiate_payment'),
    path('verify-payment/<int:event_id>/', verify_razorpay_payment, name='verify_payment'),
    path('cancel-event/<int:event_id>/', cancel_event, name='cancel_event'),
    path('payment-success/<int:event_id>/', payment_success, name='payment_success'),
    path('order/', order_menu_view, name='order_menu'),
    path('about/', about, name='about'),
    path('order/place/', place_order_view, name='place_order'),
    path('order/confirmation/<int:order_id>/', order_confirmation_view, name='order_confirmation'),
    path('order/history/', order_history_view, name='order_history'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/menus/', menu_list, name='menu_list'),
    path('admin/menus/add/', add_menu, name='add_menu'),
    path('admin/menus/edit/<int:menu_id>/', edit_menu, name='edit_menu'),
    path('admin/menus/delete/<int:menu_id>/', delete_menu, name='delete_menu'),
    path("update_event/<int:event_id>/", update_event, name="update_event"),
    path("admin/all-events/", all_events, name="all_events"),
    path('payment-success/', lambda request: render(request, 'payment_success.html'), name='payment_success'),
    path('payment-failed/', lambda request: render(request, 'payment_failed.html'), name='payment_failed'),
]
if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
