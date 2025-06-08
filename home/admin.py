from django.contrib import admin #admin model defualt
from .models import *
# Register your models here.


admin.site.register(itemCategory)#adding itemCategory to admin to change(add,delete,update)
admin.site.register(item)#item model
admin.site.register(Cart)#Registers the Cart model so that carts can be managed
admin.site.register(CartItem)# CartItem model, which likely stores individual items within a cart.
admin.site.register(Profile)#Profile model, which likely stores user profile information.
