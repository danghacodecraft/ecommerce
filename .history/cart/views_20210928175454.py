from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from store.models import Product
from django.views.decorators.http import require_POST


# Create your views here.
def cart_detail(request):
    cart = Cart(request)
    print(type(cart))
    for item in cart:
        print(item)
    return render(request, 'store/cart.html', {
        'cart': cart,
    })


@require_POST
def buy_now(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if request.POST.get('quantity'):
        cart.add(product=product, quantity=int(request.POST.get('quantity')))
    return redirect('cart:cart_detail')


@require_POST
def remove_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


@require_POST
def update_cart(request):
    cart = Cart(request)
    for item in cart:
        name = 'quantity2' + str(item['product.pk)
    return redirect('cart:cart_detail')
        
