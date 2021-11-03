from django.shortcuts import render, redirect
from customers.forms import *
from customers.models import *
from store.my_module import *
from checkout.models import Order, OrderItem
from django.contrib.auth.hashers import Argon2PasswordHasher, PBKDF2PasswordHasher

from customers.forms import FormThongTin

from .models import Customer


def login(request):
    session_status = check_session(request, 'sessionKhachHang')
    if session_status:
        return redirect('customers:my_account')

    # Lấy thông tin Tỉnh/TP... từ API
    link = 'http://api.laptrinhpython.net/vietnam'
    info = read_json(link)

    # Biến cho provinces
    provinces = []

    # Biến cho district
    data_districts = []
    data_list_districts = []

    # Biến cho ward
    data_wards = []

    for province in info:
        provinces.append(province['name'])

        # District
        districts = []
        for district in province['districts']:
            d = district['prefix'] + ' ' + district['name']
            districts.append(d)
            data_list_districts.append(d)

            # Ward
            wards = []
            for ward in district['wards']:
                w = ward['prefix'] + ' ' + ward['name']
                wards.append(w)
            else:
                data_wards.append((str(wards).replace('[', '').replace(']', '').replace("'", '').replace(', ', '|')))

        else:
            data_districts.append((str(districts).replace('[', '').replace(']', '').replace("'", '').replace(', ', '|')))

    # Đăng ký
    form = FormDangKy()
    result_regiter = ''
    if request.POST.get('btnDangKy'):
        form = FormDangKy(request.POST, Customer)

        # Kiểm tra email tồn tại hay chưa?
        email = request.POST.get('email')
        khach_hang = Customer.objects.filter(email=email)
        if khach_hang.count() > 0:
            result_regiter = '''
                <div class="alert alert-warning alert-dismissible fade show" role="alert">
                    Email đã tồn tại. Vui lòng kiểm tra lại
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                '''
        else:
            if form.is_valid() and form.cleaned_data['mat_khau'] == form.cleaned_data['xac_nhan_mat_khau']:
                # hasher = Argon2PasswordHasher()  # salt: 8 bytes
                hasher = PBKDF2PasswordHasher()  # salt: 1 bytes
                request.POST._mutable = True
                post = form.save(commit=False)
                post.ho = form.cleaned_data['ho']
                post.ten = form.cleaned_data['ten']
                post.email = form.cleaned_data['email']
                post.mat_khau = hasher.encode(form.cleaned_data['mat_khau'], '123')
                post.dien_thoai = form.cleaned_data['dien_thoai']
                post.dia_chi = form.cleaned_data['dia_chi'] + ', ' + form.cleaned_data['phuong_xa'] + ', ' \
                               + form.cleaned_data['quan_huyen'] + ', ' + form.cleaned_data['tinh_tp']

                post.save()
                result_regiter = '''
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    Đăng ký thông tin thành công.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                '''
    # Đăng nhập
    result_login = ''
    if request.POST.get('btnDangNhap'):
        # Gán biến
        email = request.POST.get('email')
        mat_khau = request.POST.get('mat_khau')
        hasher = PBKDF2PasswordHasher()
        encoded = hasher.encode(mat_khau, '123')

        # Đọc dữ liệu từ DB
        khach_hang = Customer.objects.filter(email=email, mat_khau=encoded)
        if khach_hang.count() > 0:
            # Tạo session đăng nhập của khách hàng
            request.session['sessionKhachHang'] = khach_hang.values()[0]  # dict
            return redirect('store:index')
        else:
            result_login = '''
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    Đăng nhập thất bại.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                '''

    return render(request, 'store/login.html', {
        'form': form,
        'result_regiter': result_regiter,
        'result_login': result_login,
        'provinces': tuple(provinces),
        'data_districts': tuple(data_districts),
        'data_wards': tuple(data_wards),
        'data_list_districts': data_list_districts,
    })


def my_account(request):
    update_msg = ''
    doimk_msg = ''
    session_status = check_session(request, 'sessionKhachHang')
    if not session_status:
        return redirect('customers:login')
    customer = Customer.objects.get(id=request.session['sessionKhachHang']['id'])
    form = FormThongTin(instance=customer)
    form_mk = FormDoiMatKhau()
    if request.POST.get('btnCapNhat'):
        form = FormThongTin(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            update_msg = '''
                <div class="alert alert-success alert-dismissible fade show" id="myAlert" role="alert">
                    Cập nhật thông tin thành công.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            '''
    if request.POST.get('btnMk'):
        form_mk = FormDoiMatKhau(request.POST)
        if form_mk.is_valid():
            hasher = PBKDF2PasswordHasher()
            mat_khau = hasher.encode(form_mk.cleaned_data['mat_khau'], '123')
            if mat_khau == request.session['sessionKhachHang']['mat_khau']:
                if form_mk.cleaned_data['mat_khau_moi'] == form_mk.cleaned_data['xac_nhan_mat_khau']:
                    khach_hang = Customer.objects.get(email=request.session['sessionKhachHang']['email'])

                    khach_hang.mat_khau = hasher.encode(form_mk.cleaned_data['mat_khau_moi'], '123')
                    khach_hang.save()
                    khach_hang_dict = khach_hang.__dict__
                    del(khach_hang_dict['_state'])
                    request.session['sessionKhachHang'] = khach_hang_dict
                    doimk_msg = '''
                        <div class="alert alert-success alert-dismissible fade show" id="myAlert" role="alert">
                            Đổi mật khẩu thành công.
                            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                    '''

    orders = Order.objects.filter(username=request.session['sessionKhachHang']['email'])

    return render(request, 'store/my-account.html', {
        'form': form,
        'form_mk': form_mk,
        'update_msg': update_msg,
        'doimk_msg': doimk_msg,
        'orders': orders,
        'customer': customer,
    })


def logout(request):
    if request.session.get('sessionKhachHang'):
        del request.session['sessionKhachHang']
    return redirect('customers:login')


def activate(request):
    return render()