from django.shortcuts import render, redirect
from cart.cart import Cart
from store.my_module import *
from .models import Order, OrderItem
from decimal import Decimal


def checkout(request):
    # Kiểm tra trạng thái đăng nhập của khách hàng
    session_status = check_session(request, 'sessionKhachHang')
    session_info = ''
    if session_status:
        session_info = request.session.get('sessionKhachHang')
    else:
        return redirect('cart:cart_detail')
    return render(request, 'store/checkout.html')


def success(request):
    # Kiểm tra trạng thái đăng nhập của khách hàng
    session_status = check_session(request, 'sessionKhachHang')
    session_info = ''
    if session_status:
        session_info = request.session.get('sessionKhachHang')
    else:
        return redirect('cart:cart_detail')
    cart = Cart(request)
    username = request.session['sessionKhachHang']['email']
    first_name = request.session['sessionKhachHang']['ho']
    last_name = request.session['sessionKhachHang']['ten']
    phone = request.session['sessionKhachHang']['dien_thoai']
    address = request.session['sessionKhachHang']['dia_chi']
    total = cart.get_final_total_price()
    order = Order.objects.create(username=username, first_name=first_name, last_name=last_name, phone=phone, address=address, total=total)
    order.save()

    for item in cart:
        order_item = OrderItem.objects.create(product=item['product'], order=order, price=item['total_price'], quantity=item['quantity'])
        order_item.save()
    else:
        cart.clear()

    return render(request, 'store/success.html')


