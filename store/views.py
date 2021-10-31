from django.shortcuts import render
from store.models import Category, SubCategory, Product
from store.my_module import *
from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import intcomma

# Phân trang
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# RSS
import feedparser
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from store.serializers import ProductSerializer


# SubCategory (Dùng chung)
subcategory_list = SubCategory.objects.order_by('name')


def index(request):
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
    })


def product_list(request, slug):
    # Products
    products = Product.objects.order_by('-public_day')
    if not slug == 'tat-ca-san-pham':
        subcategory = SubCategory.objects.get(slug=slug)
        products = Product.objects.filter(subcategory=subcategory).order_by('-public_day')

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

    if slug == 'tat-ca-san-pham':
        list_product = Product.objects.order_by('-public_day')
        subcategory_name = 'Tất cả sản phẩm (' + str(len(list_product)) + ')'
    else:
        selected_subcategory = SubCategory.objects.get(slug=slug)
        list_product = Product.objects.filter(subcategory=selected_subcategory).order_by('-public_day')
        subcategory_name = selected_subcategory.name + ' (' + str(len(list_product)) + ')'

    return render(request, 'store/product-list.html', {
        'subcategory_list': subcategory_list,
        'products': products_pager,
        'subcategory_name': subcategory_name,
    })


def product_detail(request, pk):

    product = Product.objects.get(pk=pk)

    # Sản phẩm liên quan
    subcategoryid = product.subcategory_id
    related_products = Product.objects.filter(subcategory=subcategoryid).exclude(id=pk).order_by('-public_day')

    # Lấy tên danh mục lên Breadcrumb
    subcategoryname = SubCategory.objects.get(id=subcategoryid)

    return render(request, 'store/product-detail.html', {
        'subcategory_list': subcategory_list,
        'product': product,
        'related_products': related_products,
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
    subcategory_name = ''
    tu_khoa = request.GET.get('tu_khoa')
    products_pager = []
    if request.GET.get('tu_khoa'):
        # Gán biến

        from_price = request.GET.get('from_price')
        to_price = request.GET.get('to_price')
        print(tu_khoa)

        if (from_price == '' and to_price == '') or (from_price is None and to_price is None):
            products_search = Product.objects.filter(name__contains=tu_khoa).order_by('-public_day')
            subcategory_name = str(len(products_search)) + ' sản phẩm với từ khóa "' + tu_khoa + '"'
        elif from_price == '' and to_price != '':
            products_search = Product.objects.filter(Q(name__contains=tu_khoa)
                                                     & Q(price__lte=int(to_price))).order_by('-public_day')
            subcategory_name = str(len(products_search)) + ' sản phẩm với từ khóa "' + \
                               tu_khoa + '"' + ' với giá dưới ' + intcomma(to_price) + 'đ'
        elif from_price != '' and to_price == '':
            products_search = Product.objects.filter(Q(name__contains=tu_khoa)
                                                     & Q(price__gte=int(from_price))).order_by('-public_day')
            subcategory_name = str(len(products_search)) + ' sản phẩm với từ khóa "' + \
                               tu_khoa + '"' + ' với giá từ ' + intcomma(from_price) + 'đ'
        else:
            products_search = Product.objects.filter(Q(name__contains=tu_khoa)
                                                     & Q(price__range=(from_price, to_price))).order_by('-public_day')
            subcategory_name = str(len(products_search)) + ' sản phẩm với từ khóa "' + \
                               tu_khoa + '"' + ' với giá từ ' + intcomma(from_price) + 'đ' + ' đến dưới ' + \
                               intcomma(to_price) + 'đ'
        # Phân trang
        products_per_page = 15
        page = request.GET.get('page', 1)
        paginator = Paginator(products_search, products_per_page)

        try:
            products_pager = paginator.page(page)
        except PageNotAnInteger:
            products_pager = paginator.page(1)
        except EmptyPage:
            products_pager = paginator.page(paginator.num_pages)

    return render(request, 'store/product-list.html', {
        'products': products_pager,
        'subcategory_name': subcategory_name,
        'tu_khoa': tu_khoa,
    })


def read_rss(request):
    newsfeed = feedparser.parse('http://feeds.feedburner.com/bedtimeshortstories/LYCF')
    return render(request, 'store/rss.html', {'newsfeed': newsfeed})


def products_service(request):
    products = Product.objects.order_by('-public_day')
    result_list = list(products.values())
    return JsonResponse(result_list, safe=False)


def product_service(request, pk):
    product = list(Product.objects.filter(id=pk).values())[0]
    return JsonResponse(product, safe=False)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.order_by('-public_day')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # permission_classes = [permissions.IsAdminUser]