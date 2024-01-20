from django.urls import path
from . import views


urlpatterns = [
    path('admin_login/',views.admin_loginn,name='admin_login'),
    path('admin_logout',views.admin_logoutt,name='admin_logout'),
    path('dashboard/',views.dashboardd,name='dashboard'),
    path('users/',views.userss,name='users'),
    path('products',views.productss,name='products'),
    path('add_product',views.add_productss,name='add_product'),
    path('category',views.categoriess,name='category'),
    path('brands',views.brandss,name='brands'),
    path('add_brands',views.add_brandss,name='add_brands'),
    path('add_category',views.add_categoryy,name='add_category'),
    path('add_variants/<str:id>/',views.add_variantss,name='add_variants'),
    path('variants/<str:id>/', views.variantss, name='variants'),
    path('edit_variants/<str:id>/',views.edit_variantss,name='edit_variants'),
    path('edit_product/<str:id>',views.edit_productss,name='edit_product'),
    path('edit_brands/<str:id>',views.edit_brandss,name='edit_brands'),
    path('edit_category/<str:id>',views.edit_categoryy,name='edit_category'),
    path('user_status/<str:id>',views.user_statuss,name='user_status'),
    path('category_status/<str:id>',views.category_statuss,name='category_status'),
    path('brand_status/<str:id>',views.brand_statuss,name='brand_status'),
    path('product_status/<str:id>',views.product_statuss,name='product_status'),
    path('variant_status/<str:id>',views.variant_statuss,name='variant_status'),
    path('admin_order/',views.admin_orderr,name='admin_order'),
    path('order_view/<str:order_id>/<str:id>/',views.order_vieww,name='order_view'),
    path('sales_report/', views.sales_report, name='sales_report'),
    path('download_exel',views.excel_report,name="download_exel"),
    # path('download_pdf',views.download_pdf,name="download_pdf"),
    path('pdf_download',views.DownloadPDF.as_view(),name='pdf_download'),
]