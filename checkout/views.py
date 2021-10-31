from django.shortcuts import render, redirect
from cart.cart import Cart
from store.my_module import *
from .models import Order, OrderItem
from django.views.decorators.http import require_POST
from EStore.settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage


def checkout(request):
    # Kiểm tra trạng thái đăng nhập của khách hàng
    session_status = check_session(request, 'sessionKhachHang')
    session_info = ''
    cart = Cart(request)
    if session_status and cart.__len__():
        session_info = request.session.get('sessionKhachHang')
    else:
        return redirect('cart:cart_detail')

    return render(request, 'store/checkout.html', {'session_info': session_info})


@require_POST
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
    subject = 'Chúc mừng ' + order.first_name + ' ' + order.last_name + ' đặt hàng thành công'
    content = '<p>' + order.address + ', tổng tiền là: ' + str(order.total) + '</p>'
    content += '''
        <table class="table">
          <thead>
            <tr>
              <th scope="col">STT</th>
              <th scope="col">Tên sản phẩm</th>
              <th scope="col">Số lượng</th>
              <th scope="col">Đơn giá</th>
              <th scope="col">Thành tiền</th>
            </tr>
          </thead>
          <tbody>'''
    for item in cart:
        content += '''<tr>
          <th scope="row">1</th>
          <td>''' + str(item['product']) + '''</td>
          <td>''' + str(item['quantity']) + '''</td>
          <td>''' + str(item['product'].price) + '''</td>
          <td>''' + str(item['total_price']) + '''</td>
        </tr>'''
    content += '''</tbody>
        </table>

    '''

    msg = EmailMessage(subject, content, EMAIL_HOST_USER, [order.username])
    msg.content_subtype = 'html'
    msg.send()

    cart.clear()

    return render(request, 'store/success.html')


