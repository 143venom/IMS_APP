from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['permissions']
        model = Group

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['email','password','company_info']

class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = '__all__'

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class BuyerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerInfo
        fields = '__all__'

class SellerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model =  SellerInfo
        fields = '__all__'

class VenderInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorInfo
        fields = '__all__'

class PurchaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseInfo
        fields = '__all__'