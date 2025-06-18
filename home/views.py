from django.shortcuts import render, redirect, get_object_or_404
from home.models import *
from django.contrib.auth.models import User 
from django.contrib.auth import login, authenticate   
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Max
from django.contrib.admin.views.decorators import staff_member_required
from .models import Item, ItemCategory
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.http import Http404
import logging
from datetime import date

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')


def home(request):
    menu = Item.objects.filter(is_available=True)  # Only show available items
    context = {
        'menu': menu
    }
    return render(request, 'home.html', context)

def login_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not username or not password:
                messages.error(request, "Please provide both username and password.")
                return redirect('/login/')

            # Check if user exists first
            if not User.objects.filter(username=username).exists():
                messages.warning(request, "User not found.")
                return redirect('/login/')

            # Authenticate the user correctly
            user_obj = authenticate(request, username=username, password=password)

            if user_obj is not None:
                login(request, user_obj)
                messages.success(request, f"Welcome back, {user_obj.username}!")
                return redirect('/')

            messages.error(request, "Wrong password.")
            return redirect('/login/')
        
        except Exception as e:
            logger.error(f"Login error: {e}")
            messages.error(request, "Something went wrong. Please try again.")
            return redirect('/login/')
    
    return render(request, 'login.html', {}) 


def register_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            department = request.POST.get('department')
            cabin_no = request.POST.get('cabin_no')
            block_no = request.POST.get('block_no')
            floor_no = request.POST.get('floor_no')
            
            if not username or not password:
                messages.error(request, "Username and password are required.")
                return redirect('/register/')
            
            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request, "Username is already taken.")
                return redirect('/register/')
            
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            
            profile = Profile.objects.get(user=user_obj)
            profile.department = department
            profile.cabin_no = cabin_no
            profile.floor_no = floor_no
            profile.block_no = block_no
            profile.save()
            
            messages.success(request, "Account created successfully. Please login.")
            return redirect('/login/')
        except Exception as e:
            logger.error(f"Registration error: {e}")
            messages.error(request, "Something went wrong. Please try again.")
            return redirect('/register/')
    
    return render(request, 'register.html')



@login_required(login_url='/login/')
def add_cart(request, food_items_uid):
    try:
        item_obj = get_object_or_404(Item, uid=food_items_uid, is_available=True)
        cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)

        # Check if the item already exists in cart
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, food_items=item_obj)
        if not item_created:  # if the item already exists in the cart, increase the quantity
            cart_item.quantity += 1
            cart_item.save()
        
        messages.success(request, f"{item_obj.item_name} added to cart!")
        return redirect('cart')
    except Exception as e:
        logger.error(f"Add to cart error: {e}")
        messages.error(request, "Failed to add item to cart.")
        return redirect('home')



@login_required(login_url='/login/')
def cart(request):
    try:
        cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
        return render(request, 'cart.html', {'cart': cart})
    except Exception as e:
        logger.error(f"Cart view error: {e}")
        messages.error(request, "Error loading cart.")
        return redirect('home')


@login_required(login_url='/login/')
def remove_cart_items(request, cart_item_uid):
    try:
        cart_item = get_object_or_404(CartItem, uid=cart_item_uid)

        if cart_item.cart.user != request.user:
            messages.error(request, "You don't have permission to modify this cart.")
            return redirect('cart') 

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            messages.success(request, f"Quantity reduced for {cart_item.food_items.item_name}")
        else:
            item_name = cart_item.food_items.item_name
            cart_item.delete()
            messages.success(request, f"{item_name} removed from cart")

        return redirect('cart')

    except CartItem.DoesNotExist:
        messages.error(request, "Item not found.")
        return redirect('cart')
    except Exception as e:
        logger.error(f"Remove cart item error: {e}")
        messages.error(request, "Something went wrong.")
        return redirect('cart')




@login_required(login_url='/login/')
def orders(request):
    try:
        orders = Cart.objects.filter(is_paid=True, user=request.user).order_by('-created_at')
        context = {'orders': orders}
        return render(request, 'orders.html', context)
    except Exception as e:
        logger.error(f"Orders view error: {e}")
        messages.error(request, "Error loading orders.")
        return redirect('home')

    
@login_required
def account_view(request):
    try:
        profile = request.user.profile
        # Calculate total orders for the user
        total_orders = Cart.objects.filter(user=request.user, is_paid=True).count()
        # Calculate days since joining
        days_active = (date.today() - request.user.date_joined.date()).days
        
        context = {
            'profile': profile,
            'total_orders': total_orders,
            'days_active': days_active
        }
        return render(request, 'account.html', context)
    except Exception as e:
        logger.error(f"Account view error: {e}")
        messages.error(request, "Error loading account.")
        return redirect('home')




def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('index')



@login_required(login_url='/login/')
def place_order(request):
    try:
        cart = get_object_or_404(Cart, user=request.user, is_paid=False)
        
        if not cart.cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('cart')
            
        cart.is_paid = True
        cart.status = 'pending'
        cart.save()
        messages.success(request, "Your order has been placed successfully!")
        return redirect('orders')
    except Cart.DoesNotExist:
        messages.error(request, "No active cart found.")
        return redirect('cart')
    except Exception as e:
        logger.error(f"Place order error: {e}")
        messages.error(request, "Failed to place order. Please try again.")
        return redirect('cart')




@staff_member_required(login_url='/login/')
def owner_dashboard(request):
    try:
        orders = Cart.objects.filter(is_paid=True).order_by('-created_at')
        context = {'orders': orders}
        return render(request, 'owner_dashboard.html', context)
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        messages.error(request, "Error loading dashboard.")
        return redirect('home')

@staff_member_required(login_url='/login/')
def update_order_status(request, order_uid):
    if request.method == "POST":
        try:
            order = get_object_or_404(Cart, uid=order_uid)
            status = request.POST.get("status")
            
            # Debug logging
            logger.info(f"Updating order {order_uid} status to: {status}")
            logger.info(f"Current order status: {order.status}")
            logger.info(f"POST data: {request.POST}")
            
            if status in ["pending", "accepted", "completed"]:
                order.status = status
                order.save()
                logger.info(f"Order status updated successfully to: {order.status}")
                messages.success(request, "Order status updated successfully.")
            else:
                logger.error(f"Invalid status received: {status}")
                messages.error(request, "Invalid status.")
        except Exception as e:
            logger.error(f"Update order status error: {e}")
            messages.error(request, "Failed to update order status.")
        return redirect('owner_dashboard')
    else:
        logger.warning(f"Non-POST request to update_order_status: {request.method}")
        return redirect('owner_dashboard')


@login_required
def profile_view(request):
    try:
        profile = request.user.profile  
        return render(request, 'profile.html', {'profile': profile})
    except Exception as e:
        logger.error(f"Profile view error: {e}")
        messages.error(request, "Error loading profile.")
        return redirect('home')



@login_required
def profile_edit(request):
    try:
        profile = request.user.profile
        if request.method == 'POST':
            department = request.POST.get('department')
            cabin_no = request.POST.get('cabin_no')
            floor_no = request.POST.get('floor_no')
            block_no = request.POST.get('block_no')

            profile.department = department
            profile.cabin_no = cabin_no
            profile.floor_no = floor_no
            profile.block_no = block_no
            profile.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')

        return render(request, 'profile_edit.html', {'profile': profile})
    except Exception as e:
        logger.error(f"Profile edit error: {e}")
        messages.error(request, "Error updating profile.")
        return redirect('profile')

@staff_member_required(login_url='/login/')
def add_item(request):
    if request.method == 'POST':
        try:
            item_name = request.POST.get('item_name')
            price = request.POST.get('price')
            images = request.FILES.get('images')
            category = request.POST.get('category')
            
            if not item_name or not price or not category:
                messages.error(request, "All fields are required.")
                return render(request, 'add_item.html')
            
            category_obj = get_object_or_404(ItemCategory, category_name=category)
            item_obj = Item.objects.create(
                item_name=item_name, 
                price=price, 
                images=images, 
                category=category_obj
            )
            messages.success(request, "Item added successfully.")
            return redirect('owner_dashboard')
        except ValidationError as e:
            messages.error(request, f"Validation error: {e}")
        except Exception as e:
            logger.error(f"Add item error: {e}")
            messages.error(request, "Failed to add item.")
    return render(request, 'add_item.html')



@staff_member_required(login_url='/login/')
def delete_item(request, food_items_uid):
    try:
        item_obj = get_object_or_404(Item, uid=food_items_uid)
        item_name = item_obj.item_name
        item_obj.delete()
        messages.success(request, f"{item_name} deleted successfully.")
    except Item.DoesNotExist:
        messages.error(request, "Item not found.")
    except Exception as e:
        logger.error(f"Delete item error: {e}")
        messages.error(request, "Failed to delete item.")
    return redirect('owner_dashboard')


@staff_member_required(login_url='/login/')
def edit_item(request, food_items_uid):
    try:
        item_obj = get_object_or_404(Item, uid=food_items_uid)
        if request.method == 'POST':
            item_name = request.POST.get('item_name')
            price = request.POST.get('price')
            images = request.FILES.get('images')

            if not item_name or not price:
                messages.error(request, "Item name and price are required.")
                return render(request, 'edit_item.html', {'item': item_obj})

            item_obj.item_name = item_name
            item_obj.price = price
            if images:
                item_obj.images = images
            item_obj.save()
            messages.success(request, "Item updated successfully.")
            return redirect('owner_dashboard')
        
        return render(request, 'edit_item.html', {'item': item_obj})
    except Exception as e:
        logger.error(f"Edit item error: {e}")
        messages.error(request, "Error editing item.")
        return redirect('owner_dashboard')



def food_items(request):
    try:
        menu = Item.objects.filter(is_available=True)
        return render(request, 'food_items.html', {'menu': menu})
    except Exception as e:
        logger.error(f"Food items error: {e}")
        messages.error(request, "Error loading menu.")
        return redirect('home')


@staff_member_required(login_url='/login/')
def delete_order(request, uid):
    try:
        order = get_object_or_404(Cart, uid=uid)  
        order.delete()
        messages.success(request, "Order deleted successfully.")
    except Exception as e:
        logger.error(f"Delete order error: {e}")
        messages.error(request, "Failed to delete order.")
    return redirect('owner_dashboard')

@login_required(login_url='/login/')
def confirm_order(request):
    try:
        cart = Cart.objects.filter(user=request.user, is_paid=False).first()
        if not cart or not cart.cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('cart')
        return render(request, 'confirm_order.html', {'cart': cart})
    except Exception as e:
        logger.error(f"Confirm order error: {e}")
        messages.error(request, "Error confirming order.")
        return redirect('cart')



@require_http_methods(["POST"])
@login_required(login_url='/login/')
def finalize_order(request):
    try:
        cart = Cart.objects.filter(user=request.user, is_paid=False).first()
        payment_method = request.POST.get('payment_method')

        if not cart or not cart.cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('cart')

        if payment_method == 'cod':
            cart.payment_method = payment_method
            cart.is_paid = True
            cart.status = 'pending'
            cart.save()
            messages.success(request, "Order placed successfully with Cash on Delivery!")
            return redirect('orders')
        elif payment_method == 'online':
            # add Razorpay or Stripe logic 
            return render(request, 'online_payment_placeholder.html', {'cart': cart})
        else:
            messages.error(request, "Invalid payment method.")
            return redirect('confirm_order')
    except Exception as e:
        logger.error(f"Finalize order error: {e}")
        messages.error(request, "Failed to process order.")
        return redirect('cart')


# Custom 404 error view for development testing
def custom_404(request, exception=None):
    return render(request, '404.html', status=404)

