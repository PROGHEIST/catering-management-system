from django.urls import path
from .views import Homepage, register_view, login_view, logout_view, dashboard, menu_list_view, add_menu_item_view, edit_menu_item_view, delete_menu_item_view, order_menu_view, place_order_view, order_confirmation_view, order_history_view, admin_dashboard_view,book_event, event_list, cancel_event, event_details, menus, menu_item, related_menu_item
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', Homepage, name='home'),
    path('menus/', menus, name='menus'),
    path('menus/<int:menu_item>', menu_item, name='menu-details'),
    path('menus/<int:related_menu_item>', related_menu_item, name='related_menu-details'),
    path('dashboard/', dashboard, name='dashboard'),
    path('admin-dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('book-event/', book_event, name='book_event'),
    path('events/', event_list, name='event_list'),
    path('events/<int:event_id>/', event_details, name='event_details'),
    path('cancel-event/<int:event_id>/', cancel_event, name='cancel_event'),
    path('menu/', menu_list_view, name='menu_list'),
    path('menu/add/', add_menu_item_view, name='add_menu_item'),
    path('menu/edit/<int:pk>/', edit_menu_item_view, name='edit_menu_item'),
    path('menu/delete/<int:pk>/', delete_menu_item_view, name='delete_menu_item'),
    path('order/', order_menu_view, name='order_menu'),
    path('order/place/', place_order_view, name='place_order'),
    path('order/confirmation/<int:order_id>/', order_confirmation_view, name='order_confirmation'),
    path('order/history/', order_history_view, name='order_history'),
]
if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
