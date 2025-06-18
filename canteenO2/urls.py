"""
URL configuration for canteenO2 project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from home.views import (
    index, login_page, place_order, register_page, add_cart, owner_dashboard, 
    update_order_status, cart, remove_cart_items, orders, home, account_view, 
    logout_view, profile_view, profile_edit, delete_item, add_item, edit_item, 
    food_items, delete_order, confirm_order, finalize_order
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Public pages
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('food_items/', food_items, name='food_items'),
    
    # Authentication
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', logout_view, name='logout'),
    
    # User features
    path('account/', account_view, name='account'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    
    # Cart and orders
    path('add-cart/<uuid:food_items_uid>/', add_cart, name='add_cart'),
    path('cart/', cart, name='cart'),
    path('remove_cart_items/<uuid:cart_item_uid>/', remove_cart_items, name='remove_cart_items'),
    path('confirm_order/', confirm_order, name='confirm_order'),
    path('finalize_order/', finalize_order, name='finalize_order'),
    path('place_order/', place_order, name='place_order'),
    path('orders/', orders, name='orders'),
    
    # Staff/Admin features
    path('dashboard/', owner_dashboard, name='owner_dashboard'),
    path('update-order-status/<uuid:order_uid>/', update_order_status, name='update_order_status'),
    path('add_item/', add_item, name='add_item'),
    path('edit_item/<uuid:food_items_uid>/', edit_item, name='edit_item'),
    path('delete_item/<uuid:food_items_uid>/', delete_item, name='delete_item'),
    path('delete_order/<uuid:uid>/', delete_order, name='delete_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

# Custom 404 handler
handler404 = 'home.views.custom_404'