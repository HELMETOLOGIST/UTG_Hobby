import datetime
import json
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as admin_login, logout as admin_logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import user_passes_test
from user_authentication.models import CustomUser
from user_products.models import Brands,Category,Products,ColorVarient,Image
from django.core.exceptions import ObjectDoesNotExist
from user_order.models import Order, OrderItem
from user_profile.models import Address
from user_cart.models import Cart
from django.utils import timezone
from datetime import date, timedelta
from django.http import JsonResponse
from django.db.models import Sum
from datetime import datetime
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from .models import *
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, F, Count, ExpressionWrapper, DecimalField
import xlwt
import datetime
from django.db.models.functions import TruncMonth, TruncYear
from user_coupon.models import Coupon, CouponUsage
# Create your views here.
############################## User Management ##############################


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_loginn(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        admin = authenticate(request, username=username,password=password)
        if admin is not None and admin.is_superuser:
            admin_login(request,admin)
            return redirect('dashboard')
        else:
            messages.error(request, "Username or Password incorrect")
            return redirect('admin_login')
    else:
        return render(request, 'admin_side/admin_login.html')  
    
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def admin_logoutt(request):
    admin_logout(request)
    return redirect('admin_login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")   
def user_statuss(request, id):
    usr = CustomUser.objects.filter(id = id).first()
    if usr.is_listed == True:
        usr.is_listed = False
        usr.save()
    else:
        usr.is_listed = True
        usr.save()
    return redirect('users')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def userss(request):
    user = CustomUser.objects.exclude(is_superuser = True).all()
    context = {
        'users' : user
    }
    return render(request, 'admin_side/users.html', context)

############################## Product Management ##############################


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def productss(request):
    product = (
        Products.objects.prefetch_related("colorvarient_set__images")
        .all()
        .order_by("id")
    )
    context = {
        'products':product
    }
    return render(request, 'admin_side/products.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def product_statuss(request,id):
    product = Products.objects.filter(id=id).first()
    if product.is_listed == True:
        product.is_listed = False
        product.save()
    else:
        product.is_listed = True
        product.save()
    return redirect('products')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def add_productss(request):
    category = Category.objects.all()
    brand = Brands.objects.all()
    if request.method == 'POST':
        product_name = request.POST.get('products_name')
        product_description = request.POST.get('product_description')
        brand_id = request.POST.get('brand')
        brand = Brands.objects.get(id=brand_id)
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        
        try:
            existing_product = Products.objects.get(products_name__iexact=product_name)
            messages.error(request, "A product with the same name already exists.")
            return redirect("add_product")
        except ObjectDoesNotExist:
            pass
        
        product = Products(
            products_name=product_name,
            description=product_description,
            category_id=category,
            brand_id=brand
        )
        product.save()
        messages.success(request, "Product added successfully.")
        return redirect('products')
    else:
        context = {
            'category':category,
            'brand':brand
        }
        return render(request, 'admin_side/add_product.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def edit_productss(request, id):
    product = get_object_or_404(Products, id=id)
    category = Category.objects.all()
    brand = Brands.objects.all()

    if request.method == 'POST':
        edit_name = request.POST.get('product_name')
        edit_desc = request.POST.get('description')
        brand_id = request.POST.get('brand')
        brand = get_object_or_404(Brands, id=brand_id)
        category_id = request.POST.get('category')
        category = get_object_or_404(Category, id=category_id)

        # Update the product instance with the new data
        product.products_name = edit_name
        product.description = edit_desc
        product.brand_id = brand
        product.category_id= category
        product.save()

        return redirect('products')  # Redirect to the product list view after editing

    context = {
        'product': product,
        'category': category,
        'brand': brand,
    }

    return render(request, 'admin_side/edit_product.html', context)



############################## Variant Management ##############################

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def variantss(request,id):
    product = get_object_or_404(Products,id=id)
    variant = ColorVarient.objects.filter(product = product)
    context = {
        "variants":variant,
        "product_id" : id
    }
    return render(request, 'admin_side/variants.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def variant_statuss(request, id):
    variant = ColorVarient.objects.filter(id=id).first()
    pro_id = variant.product.id
    if variant.is_listed == True:
        variant.is_listed = False
        variant.save()
    else:
        variant.is_listed = True
        variant.save()
    return redirect('variants', id=pro_id)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def add_variantss(request,id):
    product = get_object_or_404(Products, id=id)
    if request.method == 'POST':
        color = request.POST.get('color')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        variant = ColorVarient(
            product=product,
            color=color,
            price=price,
            quantity=quantity,
        )
        variant.save()
        for image in request.FILES.getlist("images"):
            Image.objects.create(variant=variant, image=image)
        return redirect('variants',id=id)
    
    return render(request, 'admin_side/add_variants.html', {"product":product})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def edit_variantss(request,id):
    variant = get_object_or_404(ColorVarient, id=id)
    print(variant.product.id)
    ex_img = Image.objects.filter(variant=variant).order_by("-id")
    
    if request.method == 'POST':
        color = request.POST.get('color')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        
        variant.color = color
        variant.price = price
        variant.quantity = quantity
        variant.save()
        
        new_img = request.FILES.getlist("images")
        
        if new_img:
            Image.objects.filter(variant=variant).delete()
            
            for img in new_img:
                Image.objects.create(variant=variant, image=img)
        return redirect('variants', id=variant.product.id)
    return render(
        request, "admin_side/edit_variants.html",
        {"variant":variant, "product":variant.product, "images":ex_img},
    )


############################## Category Management ##############################


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def categoriess(request):
    cat = Category.objects.all()
    context = {
        'category':cat
    }
    return render(request, 'admin_side/category.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def category_statuss(request, id):
    cat = Category.objects.filter(id = id).first()
    if cat.is_listed == True:
        cat.is_listed = False
        cat.save()
    else:
        cat.is_listed = True
        cat.save()
    return redirect('category')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def add_categoryy(request):
    if request.method == 'POST':
        cat_name = request.POST.get('category_name')
        try:
            existing_cat = Category.objects.get(name__iexact=cat_name)
            messages.error(request, "A Category with the same name already exists.")
            return redirect("add_category")
        except ObjectDoesNotExist:
            pass
        category = Category(name=cat_name, is_listed=True)
        category.save()
        return redirect('category')
    else:
        return render(request, 'admin_side/add_category.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def edit_categoryy(request, id):
    category = Category.objects.filter(id = id).first()
    if request.method == 'POST':
        edit_name = request.POST.get('edit_category')
        
        if Category.objects.filter(name=edit_name).exclude(id=category.id).exists():
            messages.error(request, "Category with this name already exists.")
        else:
            category.name = edit_name
            category.save()
            return redirect('category')
    else:
        context = {
            'category':category
        }
        return render(request, 'admin_side/edit_category.html', context)

############################## Brand Management ##############################


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def brandss(request):
    brand = Brands.objects.all()
    context = {
        "brands":brand
    }
    return render(request, 'admin_side/brands.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def brand_statuss(request, id):
    brands = Brands.objects.filter(id=id).first()
    if brands.is_listed == True:
        brands.is_listed = False
        brands.save()
    else:
        brands.is_listed =True
        brands.save()
    return redirect('brands')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def add_brandss(request):
    if request.method == 'POST':
        brand_name = request.POST.get('add_brands')
        try:
            existing_brand = Brands.objects.get(name__iexact=brand_name)
            messages.error(request, "A Brand with the same name already exists.")
            return redirect("add_brands")
        except ObjectDoesNotExist:
            pass
        brand = Brands(name=brand_name)
        brand.save()
        return redirect('brands')
    else:
        return render(request, 'admin_side/add_brands.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def edit_brandss(request, id):
    brand = Brands.objects.filter(id=id).first()
    if request.method == 'POST':
        edit_name = request.POST.get('edit_brands')
        if Brands.objects.filter(name=edit_name).exclude(id=brand.id).exists():
            messages.error(request, "Brand with this name already exists.")
        else:
            brand.name = edit_name
            brand.save()
            return redirect('brands')
    else:
        context = {
            'brand':brand
        }
        return render(request, 'admin_side/edit_brands.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def admin_orderr(request):
    order_items = OrderItem.objects.all().order_by("-id")
    return render(request, 'admin_side/orders.html', {"order_items":order_items})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def order_vieww(request, order_id, id):
    item = get_object_or_404(Order, order_id=order_id)
    order_item = OrderItem.objects.filter(order=item, id=id).first()

    if request.method == "POST":
        option = request.POST.get('options')
        if option:
            order_item.status = option
            order_item.save()

    statuses = ['Order Confirmed', 'Cancelled', 'Delivered']
    return render(request, 'admin_side/order_view.html', {'order_item': order_item, 'statuses': statuses})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def dashboardd(request):
    filter_value = request.GET.get('filter_value') #count of user,customer,revenue
    recent_activity = OrderItem.objects.all().order_by('-modified_time') #modified recent activity
    
    # Filtering the user count, revenue and customer count
    end_time = datetime.datetime.now()
    if filter_value == 'today':
        start_time = end_time - timedelta(days=1)
    elif filter_value == 'this_month':
        start_time = end_time - timedelta(weeks=1)
    elif filter_value == 'this_year':
        start_time = end_time - timedelta(days=365)
    else:
        start_time = end_time - timedelta(days=1)
        
    orders = Order.objects.filter(order_date__range=[start_time, end_time])
    
    revenue = orders.aggregate(total_revenue=Sum('total_price'))['total_revenue']
    users = orders.values('user').distinct().count()
    
    # Filtering the line_chart here
    line_value = request.GET.get('line_value', 'chart_today') #line_chart
    from django.utils import timezone

    # Assuming chart_end_time is already defined
    chart_end_time = timezone.now()

    weekday_orders = []

    for days_ago in range(6, -1, -1):  # Start from 6 days ago and go backward to 0 (today)
        start_date = chart_end_time - timedelta(days=days_ago+1)
        end_date = start_date + timedelta(days=1)

        # Fetch the count of OrderItem objects for the specified date range
        day_orders = OrderItem.objects.filter(order__order_date__range=(start_date, end_date)).count()

        # Check the count for debugging
        weekday_orders.append({'date': start_date.strftime("%A"), 'count': day_orders})

    # Month order datas
    month_orders = []
    for month in range(1, 13):
        start_date = date(chart_end_time.year, month, 1)
        if month == 12:  # Adjust end_date for December to include the year's end
            end_date = date(chart_end_time.year + 1, 1, 1)
        else:
            end_date = date(chart_end_time.year, month + 1, 1)
        month_orders.append({'date': start_date.strftime("%B"), 'count': OrderItem.objects.filter(order__order_date__range=(start_date, end_date)).count()})
        month_orders = month_orders[::-1]
    # Year order datas
    year_orders = []
    for year in range(2024, 2018, -1):
        year_orders.append({'date': year, 'count': OrderItem.objects.filter(order__order_date__year=year).count()})
        year_orders = year_orders[::-1]

    chart_start_time = chart_end_time - timedelta(days=1)

    # Fetch order counts based on the selected time range
    orders_chart = Order.objects.filter(order_date__range=[chart_start_time, chart_end_time])
    order_counts = {
        'day': orders_chart.filter(order_date__date=chart_end_time.date()).count(),
        'month': orders_chart.filter(order_date__month=chart_end_time.month).count(),
        'year': orders_chart.filter(order_date__year=chart_end_time.year).count(),
    }
    # Round Graph for most buyed category and payment method 
    payment_method_counts = Order.objects.values('payment_mode').annotate(count=Count('payment_mode'))
    category_method_counts = Category.objects.annotate(count=Count('products')).order_by('-count')
    category_counts_list = list(category_method_counts.values('name', 'count'))

    # Pass the order counts and other context data to the template
    context = {
        'revenue': revenue,
        'users': users,
        'orders': orders.count(),
        'start_time': start_time,
        'end_time': end_time,
        'recent_activity': recent_activity,
        'orders_chart': orders_chart.count(),
        'chart_start_time': chart_start_time,
        'chart_end_time': chart_end_time,
        'order_counts': order_counts,
        'line_value': line_value,
        'payment_method_counts_json': json.dumps(list(payment_method_counts)),
        'category_counts_list_json':json.dumps(list(category_counts_list)),
        'weekday_orders_json':json.dumps(list(weekday_orders)),
        'month_orders_json':json.dumps(list(month_orders)),
        'year_orders_json':json.dumps(list(year_orders)),
    }
    
    return render(request, 'admin_side/dashboard.html', context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def sales_report(request):
    # Get start_date and end_date from request parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Initialize a queryset with all OrderItems
    items = OrderItem.objects.all().order_by("-order__order_date")

    # Check if start_date and end_date are provided for filtering
    if start_date and end_date:
        # Filter orders based on the provided date range
        items = items.filter(order__order_date__range=[start_date, end_date])

    context = {
        'items': items,
    }

    return render(request, 'admin_side/sales_report.html', context)


def excel_report(request):
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = (
        "attachment; filename=SalesReport-" + str(datetime.datetime.now()) + "-.xls"
    )
    work_b = xlwt.Workbook(encoding="utf-8")
    work_s = work_b.add_sheet("SalesReport")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = [
        "Order ID",
        "User",
        "Date",
        "Time",
        "Product",
        "Color",
        "Quantity",
        "Price",
        "Payment Mode",
        "Total Price",  # Add the "Total Price" column
    ]

    for column_num in range(len(columns)):
        work_s.write(row_num, column_num, columns[column_num], font_style)
    font_style = xlwt.XFStyle()

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if not start_date:
        start_date = datetime.datetime.now() - timedelta(days=3 * 365)

    if not end_date:
        end_date = datetime.datetime.now()

    orders = (
        Order.objects.all()
        .order_by("-order_date")
        .filter(order_date__range=[start_date, end_date])
        .values_list(
            # Use the correct field name here (e.g., "orderitem__variant__product__products_name")
            "order_id",
            "user__first_name",
            "order_date__date",
            "order_date__time",
            "orderitem__variant__product__products_name",  # Assuming the correct field is "orderitem"
            "orderitem__variant__color",
            "orderitem__quantity",
            "orderitem__price",
            "payment_mode",
        )
    )

    total_price = 0  # Initialize total price
    for order in orders:
        row_num += 1
        for col_num in range(len(order)):
            work_s.write(row_num, col_num, str(order[col_num]), font_style)
        total_price += order[7]  # Add the price of each order to the total

    # Write the total price in the last row
    work_s.write(row_num + 1, 8, str(total_price), font_style)

    work_b.save(response)

    return response

    
 
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None   


class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        if start_date == "":
            start_date = datetime.datetime.now() - timedelta(days=3 * 365)
        if end_date == "":
            end_date = datetime.datetime.now()

        orders = Order.objects.all().order_by("-order_date").filter(order_date__range=[start_date, end_date])

        # Calculate the total price
        total_price = sum(order.total_price for order in orders)

        data = {
            "company": "UTG Hobby",
            "address": start_date,
            "city": "Calicut",
            "state": "Kerala",
            "zipcode": "673006",
            "orders": orders,
            "phone": end_date,
            "email": "nijithckv2001@gmail.com",
            "website": "utghobby.com",
            "total_price": total_price,  # Pass the total price to the context
        }

        pdf = render_to_pdf("admin_side/sales_report_pdf.html", data)

        response = HttpResponse(pdf, content_type="application/pdf")
        filename = f"Sales_report_{datetime.datetime.now()}.pdf"
        content = "attachment; filename=%s" % (filename)
        response["Content-Disposition"] = content
        return response

    
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def banner(request):
    banner = Banner.objects.all().order_by("-id")
    print(banner)
    return render(request, 'admin_side/banner.html', {'banner':banner})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def add_banner(request):
    products = ColorVarient.objects.filter(is_listed=True).order_by("id")
    if request.method == "POST":
        title = request.POST.get("title")
        subtitle = request.POST.get("subtitle")
        product = request.POST.get("product")
        image = request.FILES.get("images")
        variant = get_object_or_404(ColorVarient, pk=product)
        print(product)
        print(variant)
        
        Banner.objects.create(
            title = title,
            subtitle = subtitle,
            variant = variant,
            image = image,
        )
        return redirect('banner')
    return render(request, 'admin_side/add_banner.html', {'products':products})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def edit_banner(request,id):
    banner = get_object_or_404(Banner, pk=id)
    products = ColorVarient.objects.filter(is_listed=True).order_by("id")
    
    if request.method == "POST":
        title = request.POST.get("title")
        subtitle = request.POST.get("subtitle")
        product = request.POST.get("product")
        image = request.FILES.get("images")
        variant = get_object_or_404(ColorVarient, pk=product)
        
        banner.title = title
        banner.subtitle = subtitle
        banner.variant = variant
        
        if image:
            banner.image = image
        banner.save()
        return redirect('banner')
    context = {
        "banner":banner,
        "products":products,
    }
    return render(request, 'admin_side/edit_banner.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def banner_status(request,id):
    banner = Banner.objects.filter(id=id).first()
    
    if banner.is_listed == True:
        banner.is_listed = False
        banner.save()
    else:
        banner.is_listed = True
        banner.save()
    return redirect('banner')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def coupon(request):
    coupons = Coupon.objects.all().order_by("id")
    context = {
        "coupons":coupons,
    }
    return render(request, 'admin_side/coupon.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def add_coupon(request):
    if request.method == "POST":
        name = request.POST["name"]
        code = request.POST["code"]
        discount_price = request.POST["discount_price"]
        minimum_purchase = request.POST["minimum_purchase"]
        exp_date = request.POST["exp_date"]
        usage_limit = request.POST["usage_limit"]
        
        if Coupon.objects.filter(name=name).exists():
            messages.error(request, "Name already added")
            return redirect("coupon")

        if Coupon.objects.filter(code=code).exists():
            messages.error(request,"Code is already added")
            return redirect("coupon")
        
        Coupon.objects.create(
            name = name,
            code = code,
            discount_price = int(discount_price),
            minimum_purchase = float(minimum_purchase),
            exp_date = exp_date,
            usage_limit = int(usage_limit),
        )
        return redirect("coupon")
    
    return render(request, 'admin_side/add_coupon.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def edit_coupon(request,id):
    coupon = Coupon.objects.filter(id=id).first()
    if request.method == "POST":
        name = request.POST["name"]
        code = request.POST["code"]
        discount_price = request.POST["discount_price"]
        minimum_purchase = request.POST["minimum_purchase"]
        exp_date = request.POST["exp_date"]
        usage_limit = request.POST["usage_limit"]
        
        if Coupon.objects.filter(name=name).exclude(id=id).exists():
            messages.error(request,"Name already exists")
            return redirect("edit_coupon", id=id)
        
        if Coupon.objects.filter(code=code).exclude(id=id).exists():
            messages.error(request,"Code already exists")
            return redirect("edit_coupon", id-id)
        
        coupon.name = name
        coupon.code = code
        coupon.discount_price = discount_price
        coupon.minimum_purchase = float(minimum_purchase)
        coupon.exp_date = exp_date
        coupon.usage_limit = int(usage_limit)
        coupon.save()
        return redirect("coupon")
        
    context = {
        'coupon':coupon,
    }
        
    return render(request, 'admin_side/edit_coupon.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def coupon_status(request,id):
    coupon = Coupon.objects.filter(id=id).first()
    if coupon.is_active == True:
        coupon.is_active = False
        coupon.save()
    else:
        coupon.is_active = True
        coupon.save()
    return redirect("coupon")




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def offers(request):
    variant = ColorVarient.objects.filter(product_offer__gt=0)
    return render(request, 'admin_side/offer.html', {'variant':variant})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def add_offer(request):
    products = ColorVarient.objects.all().order_by('id')
    if request.method == "POST":
        product = request.POST.get('product')
        discount =request.POST.get('discount')
        
        variant = get_object_or_404(ColorVarient, id=product)
        variant.product_offer = discount
        variant.save()
        return redirect('offers')
    return render(request, 'admin_side/add_offer.html', {'products':products})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def edit_offer(request,id):
    product = ColorVarient.objects.all().order_by('id')
    item = get_object_or_404(ColorVarient, id=id)
    if request.method == "POST":
        discount = request.POST.get('discount')
        
        item.product_offer = discount
        item.save()
        return redirect('offers')
    return render(request, 'admin_side/edit_offer.html', {'item':item,'products':product})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def offer_delete(request,id):
    item = get_object_or_404(ColorVarient, id=id)
    item.product_offer = 0
    item.save()
    return redirect('offers')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def category_offer(request):
    category = ColorVarient.objects.filter(category_offer__gt=0)
    return render(request, 'admin_side/category_offer.html', {'category':category})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def add_category_offer(request):
    categories = Category.objects.all().order_by('id')
    
    if request.method == "POST":
        category_id = request.POST.get('category')
        discount = request.POST.get('discount')
        
        # Get the selected Category
        category = get_object_or_404(Category, id=category_id)
        
        # Update category_offer for all ColorVarients associated with the selected Category
        color_varients = ColorVarient.objects.filter(product__category_id=category_id)
        color_varients.update(category_offer=discount)
        
        return redirect('category_offer')
    
    return render(request, 'admin_side/add_category_offer.html', {'categories': categories})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def edit_category_offer(request,id):
    categories = Category.objects.all().order_by('id')
    item = get_object_or_404(ColorVarient, id=id)
    print(item)
    if request.method == "POST":
        discount = request.POST.get('discount')

        item.category_offer = discount
        
        return redirect('category_offer')
    
    return render(request, 'admin_side/edit_category_offer.html', {'categories': categories, 'item':item})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def cancel_category_offer(request,id):
    item = get_object_or_404(ColorVarient, id=id)
    item.category_offer = 0
    item.save()
    return redirect('category_offer')