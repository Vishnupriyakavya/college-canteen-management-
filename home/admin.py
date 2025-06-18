from django.contrib import admin #admin model defualt
from .models import ItemCategory, Item, Cart, CartItem, Profile
# Register your models here.


admin.site.register(ItemCategory)#adding itemCategory to admin to change(add,delete,update)
admin.site.register(Item)#item model
admin.site.register(Cart)#Registers the Cart model so that carts can be managed
admin.site.register(CartItem)# CartItem model, which likely stores individual items within a cart.
admin.site.register(Profile)#Profile model, which likely stores user profile information.
