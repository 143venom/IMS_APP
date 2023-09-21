from django.urls import path
from .views import *


urlpatterns = [
    path('company_info/',CompanyInfoApiView.as_view(),name='company info'),
    path('company_info/<int:pk>/',CompanyInfoIdApiView.as_view(),name='company info detail'),
    path('login/',login,name='login'),
    path('register/',register,name='register'),
    path('admin-create/',admin_create,name='admin-create'),
    path('group/',GroupApiView.as_view(),name='group list'),
    path('product_type/',productTypeApiView.as_view(),name='product type list'),
    path('product_info/',ProductsApiView.as_view(),name='product list'),
    path('buyer_info/',BuyerInfoApiView.as_view(),name='buyer list'),
    path('seller_info',SellerInfoApiView.as_view,name='seller list'),
    path('vendor_info',VendorInfoApiView.as_view,name='vendor list'),
    path('purchase-info',PurchaseInfoApiView.as_view,name='purhase list')
]