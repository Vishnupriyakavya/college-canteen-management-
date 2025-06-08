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
from .models import item, itemCategory
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'index.html')


def home(request):
    menu=item.objects.all()  # Fetches all items from the database
    context={
        'menu':menu
        } # passes the list of items to the home
    return render(request,'home.html',context)

def login_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Check if user exists first
            if not User.objects.filter(username=username).exists():
                messages.warning(request, "User not found.")
                return redirect('/login/')

            # Authenticate the user correctly
            user_obj = authenticate(request, username=username, password=password)

            if user_obj is not None:
                login(request, user_obj)
                return redirect('/')

            messages.error(request, "Wrong password.")
            return redirect('/login/')
        
        except Exception as e:
            messages.error(request, "Something went wrong.")
            return redirect('/register/')
    
    return render(request, 'login.html', {}) 


def register_page(request):
    if request.method == 'POST':
        try:
            username=request.POST.get('username')
            password=request.POST.get('password')
            department = request.POST.get('department')
            cabin_no = request.POST.get('cabin_no')
            block_no = request.POST.get('block_no')
            floor_no = request.POST.get('floor_no')
            user_obj=User.objects.filter(username=username)
            if user_obj.exists():
                messages.error(request, "User name is taken.")
                return redirect('/register/')
            
            user_obj=User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            profile = Profile.objects.get(user=user_obj)
            profile.department = department
            profile.cabin_no = cabin_no
            profile.floor_no = floor_no
            profile.block_no = block_no
            profile.save()
            messages.success(request, "Account created successfully.")
            return redirect('/login/')
        except Exception as e:
            messages.error(request, "Something went wrong.")
            return redirect('/register/')
    
    return render(request,'register.html')



@login_required(login_url='/login/')
def add_cart(request, food_items_uid):
    item_obj = item.objects.get(uid=food_items_uid)
    cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)

    # Check if the item already exists in cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart,food_items=item_obj)
    if not item_created:                  #if the item already exists in the cart, increase the quantity item created is false
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart')



@login_required(login_url='/login/')
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user, is_paid=False)
    return render(request, 'cart.html', {'carts': cart})


@login_required(login_url='/login/')
def remove_cart_items(request, cart_item_uid):
    try:
        cart_item = CartItem.objects.get(uid=cart_item_uid)

        if cart_item.cart.user != request.user:
            return redirect('cart') 

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

        return redirect('cart')

    except CartItem.DoesNotExist:
        messages.error(request, "Item not found.")
        return redirect('cart')
    except Exception as e:
        print(e)
        messages.error(request, "Something went wrong.")
        return redirect('cart')




@login_required(login_url='/login/')
def orders(request):
    
    orders= Cart.objects.filter(is_paid=True,user=request.user)
    context={'orders':orders}
    return render(request, 'orders.html',context)

    
@login_required
def account_view(request):
    return render(request, 'account.html', {'user': request.user})




def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('index')  
    return redirect('index')  



@login_required(login_url='/login/')
def place_order(request):
    try:
        cart = Cart.objects.get(user=request.user, is_paid=False)
        cart.is_paid = True
        cart.status = 'pending'
        cart.save()
        messages.success(request, "Your order has been placed successfully!")
        return redirect('orders')
    except Cart.DoesNotExist:
        messages.error(request, "No active cart found.")
        return redirect('cart')




@staff_member_required(login_url='/login/')
def owner_dashboard(request):
    orders = Cart.objects.filter(is_paid=True).order_by('-created_at')
    context = {'orders': orders}
    return render(request, 'owner_dashboard.html', context)


@staff_member_required(login_url='/login/')
def update_order_status(request, order_uid):
>>>>>>> fb557b8 (Added new features)
    if request.method == "POST":
        order = get_object_or_404(Cart, uid=order_uid)
        status = request.POST.get("status")
        if status in ["pending", "accepted", "completed"]:
            order.status = status
            order.save()
            messages.success(request, "Order status updated.")
        else:
            messages.error(request, "Invalid status.")
        return redirect('owner_dashboard')


@login_required
def profile_view(request):
    profile = request.user.profile  
    return render(request, 'profile.html', {'profile': profile})



@login_required
def profile_edit(request):
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

@staff_member_required(login_url='/login/')
def add_item(request):
    if request.method=='POST':
        item_name = request.POST.get('item_name')
        price = request.POST.get('price')
        images= request.FILES.get('images')
        
        category= request.POST.get('category')
        category_obj = itemCategory.objects.get(category_name=category)
        item_obj = item.objects.create(item_name=item_name, price=price, images=images, category=category_obj)
        item_obj.save()
        messages.success(request, "Item added successfully.")
        return redirect('owner_dashboard')
    return render(request, 'add_item.html')



@staff_member_required(login_url='/login/')
def delete_item(request, food_items_uid):
    try:
        item_obj = item.objects.get(uid=food_items_uid)
        item_obj.delete()
        messages.success(request, "Item deleted successfully.")
    except item.DoesNotExist:
        messages.error(request, "Item not found.")
    return redirect('owner_dashboard')


@staff_member_required(login_url='/login/')
def edit_item(request, food_items_uid):
    item_obj = get_object_or_404(item, uid=food_items_uid)
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        price = request.POST.get('price')
        images = request.FILES.get('images')

        item_obj.item_name = item_name
        item_obj.price = price
        if images:
            item_obj.images = images
        item_obj.save()
        messages.success(request, "Item updated successfully.")
        return redirect('owner_dashboard')
    
    return render(request, 'edit_item.html', {'item': item_obj})



def food_items(request):
    menu = item.objects.all()
    return render(request, 'food_items.html', {'menu': menu})
<<<<<<< HEAD
=======



@staff_member_required(login_url='/login/')
def delete_order(request, uid):
    order = get_object_or_404(Cart, uid=uid)  
    order.delete()
    messages.success(request, "Order deleted successfully.")
    return redirect('owner_dashboard')

def confirm_order(request):
    cart = Cart.objects.filter(user=request.user, is_paid=False).first()
    if not cart:
        return redirect('cart')
    return render(request, 'confirm_order.html', {'cart': cart})



@csrf_exempt
def finalize_order(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(user=request.user, is_paid=False).first()
        payment_method = request.POST.get('payment_method')

        if not cart:
            return redirect('cart')

        if payment_method == 'cod':
            cart.payment_method = payment_method
            cart.is_paid = True
            cart.status = 'pending'
            cart.save()
            return redirect('orders')
        elif payment_method == 'online':
            # add Razorpay or Stripe logic 
            return render(request, 'online_payment_placeholder.html', {'cart': cart})
    return redirect('cart')
>>>>>>> fb557b8 (Added new features)
