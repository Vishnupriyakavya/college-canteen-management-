from django.db import models
from django.contrib.auth.models import User, AbstractUser  # For User and AbstractUser models
from django.contrib.auth import login, authenticate  # For authentication functions
from django.contrib import messages
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
import uuid                     # module to generate universally unique IDs for objects


class BaseModel(models.Model):#abstract base class for common fields // models	A module  //Model	A class inside that module
    # This class will be inherited by other models to have common fields
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)#automatically sets the field to now when the object is created.
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:  #not created as a table ,fields are inherited by other models
        abstract = True

class ItemCategory(BaseModel):#Represents a category of items 
    category_name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.category_name  #Returns the category name when the object is printed



class Item(BaseModel):
    category=models.ForeignKey(ItemCategory,on_delete=models.CASCADE,related_name='items')
    item_name = models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    images=models.ImageField(upload_to='items')
    is_available = models.BooleanField(default=True)
    
    def __str__(self):#Returns the item name when the object is printed
        return self.item_name

class Cart(BaseModel):
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name='carts')
    is_paid=models.BooleanField(default=False)# means the user has not checked out.
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'),('accepted', 'Accepted'),('completed', 'Completed')],
        default='pending'
    )
    payment_method = models.CharField( 
        max_length=20,
        choices=[('cod', 'Cash on Delivery'), ('online', 'Online Payment')],
        null=True,
        blank=True
    )
    
    def get_cart_total(self):
        try:
            return sum(item.get_total_price() for item in self.cart_items.all())
        except:
            return 0
    
    def __str__(self):
        return f"Cart {self.uid} - User: {self.user.username if self.user else 'Anonymous'}"


class CartItem(BaseModel):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_items')
    food_items=models.ForeignKey(Item,on_delete=models.CASCADE)#Represents an item inside a specific cart.
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    
    def get_total_price(self):
        try:
            return self.food_items.price * self.quantity
        except:
            return 0
    
    def __str__(self):
        return f"{self.food_items.item_name} - Quantity: {self.quantity}"
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    cabin_no = models.CharField(max_length=10, blank=True, null=True)
    block_no = models.CharField(max_length=10, blank=True, null=True)
    floor_no = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.user.username




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

