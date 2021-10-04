from django.shortcuts import render
from store.models import Category, SubCategory, Product
from django.db.models import Q
from store.my_module import *

# Phân trang
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# SubCategory (Dùng chung)
subcategory_list = SubCategory.objects.order_by('name')


# Create your views here.
# def index_2(request):
#     # Kiểm tra trạng thái đăng nhập của khách hàng
#     session_status = check_session(request, 'sessionKhachHang')
#     session_info = ''
#     if session_status:
#         session_info = request.session.get('sessionKhachHang')

#     # Đồ dùng nhà bếp
#     category_ddnb = Category.objects.get(pk=2)

#     # Thiết bị gia đình
#     category_tbgd = Category.objects.get(pk=1)

#     return render(request, 'store/index-2.html', {
#         'category_ddnb': category_ddnb,
#         'category_tbgd': category_tbgd,
#         'session_status': session_status,
#         'session_info': session_info,
#     })


def index(request):
    # Kiểm tra trạng thái đăng nhập của khách hàng
    session_status = check_session(request, 'sessionKhachHang')
    session_info = ''
    if session_status:
        session_info = request.session.get('sessionKhachHang')

    # Thiết bị gia đình
    subcategory_ttgd = SubCategory.objects.filter(category=1).values_list('id')
    list_subcategoryid_tbgd = []
    for item in subcategory_ttgd:
        list_subcategoryid_tbgd.append(item[0])
    list_product_tbgd = Product.objects.filter(subcategory__in=list_subcategoryid_tbgd).order_by('-public_day')[:21]

    # Đồ dùng nhà bếp
    subcategory_ddnb = SubCategory.objects.filter(category=2).values_list('id')
    list_subcategoryid_ddnb = []
    for item in subcategory_ddnb:
        list_subcategoryid_ddnb.append(item[0])
    list_product_ddnb = Product.objects.filter(subcategory__in=list_subcategoryid_ddnb).order_by('-public_day')[:21]

    return render(request, 'store/index.html', {
        'list_product_tbgd': list_product_tbgd,
        'list_product_ddnb': list_product_ddnb,
        'session_status': session_status,
        'session_info': session_info,
    })


# def index(request):
#     # Đồ dùng nhà bếp
#     category_ddnb = Category.objects.get(pk=2)

#     # Thiết bị gia đình
#     category_tbgd = Category.objects.get(pk=1)

#     value = 1

#     print(request.COOKIES.get('visits'))
#     if request.COOKIES.get('visits'):
#         value = int(request.COOKIES.get('visits'))

#     response = render(request, 'store/index.html', {
#         'category_ddnb': category_ddnb,
#         'category_tbgd': category_tbgd,
#         'visits': value,
#     })

#     if value >= 1:
#         response.set_cookie('visits', value + 1)
#     else:
#         response.set_cookie('visits', value)
#     # response.delete_cookie('visits')

#     return response


def product_list(request, pk):
    # Kiểm tra trạng thái đăng nhập của khách hàng
    session_status = check_session(request, 'sessionKhachHang')
    session_info = ''
    if session_status:
        session_info = request.session.get('sessionKhachHang')

    # Products
    products = Product.objects.order_by('-public_day')
    if pk != 0:
        products = Product.objects.filter(subcategory_id=pk).order_by('-public_day')

    # Phân trang
    products_per_page = 15
    page = request.GET.get('page', 1)
    paginator = Paginator(products, products_per_page)

    try:
        products_pager = paginator.page(page)
    except PageNotAnInteger:
        products_pager = paginator.page(1)
    except EmptyPage:
        products_pager = paginator.page(paginator.num_pages)

    if pk == 0:
        list_product = Product.objects.order_by('-public_day')
        subcategory_name = 'Tất cả sản phẩm (' + str(len(list_product)) + ')'
    else:
        list_product = Product.objects.filter(subcategory=pk).order_by('-public_day')
        selected_subcategory = SubCategory.objects.get(pk=pk)
        subcategory_name = selected_subcategory.name + ' (' + str(len(list_product)) + ')'

    return render(request, 'store/product-list.html', {
        'subcategory_list': subcategory_list,
        'products': products_pager,
        'subcategory_name': subcategory_name,
        'session_status': session_status,
        'session_info': session_info,
    })


def product_detail(request, pk):
    # Kiểm tra trạng thái đăng nhập của khách hàng
    session_status = check_session(request, 'sessionKhachHang')
    session_info = ''
    if session_status:
        session_info = request.session.get('sessionKhachHang')

    product = Product.objects.get(pk=pk)

    # Sản phẩm liên quan
    subcategoryid = product.subcategory_id
    # related_products = Product.objects.filter(Q(subcategory_id=subcategoryid)).order_by('-public_day')
    related_products = Product.objects.filter(subcategory=subcategoryid).exclude(id=pk).order_by('-public_day')

    # Lấy tên danh mục lên Breadcrumb
    subcategoryname = SubCategory.objects.get(id=subcategoryid)

    return render(request, 'store/product-detail.html', {
        'subcategory_list': subcategory_list,
        'product': product,
        'related_products': related_products,
        'session_status': session_status,
        'session_info': session_info,
        'subcategoryid': subcategoryid,
        'subcategoryname': subcategoryname,
    })


def contact(request):
    # Kiểm tra trạng thái đăng nhập của khách hàng
    session_status = check_session(request, 'sessionKhachHang')
    session_info = ''
    if session_status:
        session_info = request.session.get('sessionKhachHang')

    return render(request, 'store/contact.html', {
        'session_status': session_status,
        'session_info': session_info,
    })


def search(request):
    # Kiểm tra trạng thái đăng nhập của khách hàng
    session_status = check_session(request, 'sessionKhachHang')
    session_info = ''
    if session_status:
        session_info = request.session.get('sessionKhachHang')

    product_name = ''
    products_pager = []
    if request.GET.get('product_name'):
        # Gán biến
        product_name = request.GET.get('product_name')
        products_search = Product.objects.filter(name__contains=product_name).order_by('-public_day')
        product_price = Product.objects.filter(name__b)

        # Phân trang
        products_per_page = 15
        page = request.GET.get('page', 1)
        paginator = Paginator(products_search, products_per_page)

        subcategory_name = str(len(products_search)) + ' sản phẩm với từ khóa "' + product_name + '"'
        list_product_sidebar = products_search

        try:
            products_pager = paginator.page(page)
        except PageNotAnInteger:
            products_pager = paginator.page(1)
        except EmptyPage:
            products_pager = paginator.page(paginator.num_pages)

    return render(request, 'store/product-list.html', {
        'products': products_pager,
        'subcategory_name': subcategory_name,
        'product_name': product_name,
        'session_status': session_status,
        'session_info': session_info,
    })
