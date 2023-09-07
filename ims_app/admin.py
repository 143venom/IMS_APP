from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CompanyInfo)
admin.site.register(UserInfo)
admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(BuyerInfo)
admin.site.register(SellerInfo)
admin.site.register(VendorInfo)
admin.site.register(PurchaseInfo)