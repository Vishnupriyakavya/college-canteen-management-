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
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from home.views import index, login_page,place_order, register_page, add_cart,owner_dashboard, update_order_status, cart, remove_cart_items, orders, home, account_view, logout_view,profile_view, profile_edit,delete_item,add_item,edit_item,food_items
from django.contrib.auth.views import LogoutView




urlpatterns = [
     path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('home/', home, name='home'),
    
    path('login/',login_page,name='login'),
    path('register/',register_page,name='register'),
    path('add-cart/<food_items_uid>',add_cart,name='add_cart'),
    path('cart/',cart,name='cart'),
    path('remove_cart_items/<cart_item_uid>/',remove_cart_items,name='remove_cart_items'),
    path('orders/',orders,name='orders'),

   
    path('account/', account_view, name='account'),
   path("logout/", logout_view, name="logout"),
   path('place_order/', place_order, name='place_order'),
    path('dashboard/', owner_dashboard, name='owner_dashboard'),
    path('update-order-status/<uuid:order_uid>/', update_order_status, name='update_order_status'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('delete_item/<food_items_uid>/', delete_item, name='delete_item'),
    path('add_item/', add_item, name='add_item'),
    path('edit_item/<food_items_uid>/', edit_item, name='edit_item'),
    path('food_items/', food_items, name='food_items')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()