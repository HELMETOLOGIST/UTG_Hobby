from user_cart.models import Cart
def username(request):
    try:
        firstname = request.user.first_name
        return {
            "first_name" : firstname
        }
    except:
        return {}
        
# def cartCount(request):
#     try:
#         count = Cart.objects.filter(prod_quantity=request.user).count()
#         return {
#             'totalItems': count,
#         }
#     except:
#         return {'totalItems':'0'}  
    


from user_cart.models import Cart  # Import your Cart model

def cart_count(request):
    if request.user.is_authenticated:
        # Assuming you have a ForeignKey from Cart to User
        cart_count = Cart.objects.filter(user=request.user).count()
    else:
        # Handle the case for anonymous users or adjust as needed
        cart_count = 0

    return {'cart_count': cart_count}
        
