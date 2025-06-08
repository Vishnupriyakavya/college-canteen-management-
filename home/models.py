from django.db import models
from django.contrib.auth.models import User, AbstractUser  # For User and AbstractUser models
from django.contrib.auth import login, authenticate  # For authentication functions
from django.contrib import messages
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid                     # module to generate universally unique IDs for objects


class BaseModel(models.Model):#abstract base class for common fields // models	A module  //Model	A class inside that module
    # This class will be inherited by other models to have common fields
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)#automatically sets the field to now when the object is created.
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:  #not created as a table ,fields are inherited by other models
        abstract = True

class itemCategory(BaseModel):#Represents a category of items 
    category_name = models.CharField(max_length=100)
    def __str__(self):
        return self.category_name  #Returns the category name when the object is printed



class item(BaseModel):
    category=models.ForeignKey(itemCategory,on_delete=models.CASCADE,related_name='items')
    item_name = models.CharField(max_length=100)
    price=models.FloatField()
    images=models.ImageField(upload_to='items')
    def __str__(self):#Returns the item name when the object is printed
        return self.item_name

class Cart(BaseModel):
    user=models.ForeignKey(User,null=True,blank=True,on_delete=models.SET_NULL,related_name='Carts')
    is_paid=models.BooleanField(default=False)# means the user has not checked out.
    created_at = models.DateTimeField(auto_now_add=True)
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
        return sum(item.get_total_price() for item in self.Cart_item.all())
    def __str__(self):
        return f"Cart {self.uid} - User: {self.user.username if self.user else 'Anonymous'} - Total: {self.get_cart_total()}"


class CartItem(BaseModel):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='Cart_item')
    food_items=models.ForeignKey(item,on_delete=models.CASCADE)#Represents an item inside a specific cart.
    quantity = models.PositiveIntegerField(default=1)
    def get_total_price(self):
        return self.food_items.price * self.quantity
    def __str__(self):
        return f"{self.food_items.item_name} - Quantity: {self.quantity} - Total: {self.get_total_price()} - User: {self.cart.user.username if self.cart.user else 'Anonymous'}"
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

