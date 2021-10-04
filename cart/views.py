from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Cart
from store.models import Product
from django.views.decorators.http import require_POST


# Create your views here.
def cart_detail(request):

    # Giỏ hàng
    cart = Cart(request)

    # Xử lý cập nhật dữ liệu
    if request.POST.get('btnUpdateCart'):
        cart_new = {}
        for item in cart:
            quantity_new = int(request.POST.get('quantity2_' + str(item['product'].pk)))
            if quantity_new != 0:
                product_new = {
                    str(item['product'].pk): {
                        'quantity': quantity_new,
                        'price': str(item['product'].price),
                        'coupon': '1'
                    }
                }
                cart_new.update(product_new)
            else:
                cart.remove((item['product']))
            item['quantity'] = quantity_new
        else:
            request.session['cart'] = cart_new

    print(request.session.get('cart'))

    return render(request, 'store/cart.html', {'cart': cart})


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



