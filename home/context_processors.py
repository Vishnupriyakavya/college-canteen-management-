from django.db.models import Sum
from .models import Cart

def cart_count(request):
    """Add cart count to all templates"""
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.filter(user=request.user, is_paid=False).first()
            if cart:
                count = cart.cart_items.aggregate(total=Sum('quantity'))['total'] or 0
                return {'cart_count': count}
            return {'cart_count': 0}
        except:
            return {'cart_count': 0}
    return {'cart_count': 0} 