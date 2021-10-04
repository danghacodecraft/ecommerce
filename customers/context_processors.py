from store.my_module import *
from cart.cart import Cart


def check_authenticate(request):
    cart = Cart(request)

    session_status = check_session(request, 'sessionKhachHang')
    session_info = ''
    if session_status:
        session_info = request.session.get('sessionKhachHang')

    return {
        'cart': cart,
        'session_status': session_status,
        'session_info': session_info,
    }