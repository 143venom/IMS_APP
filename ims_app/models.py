from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CompanyInfo(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    logo = models.ImageField(null=True,blank=True)
    address = models.TextField()
    email = models.EmailField(unique=True)
    contact_no = models.IntegerField() 

    def __str__(self):
        return self.name

class UserInfo(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    username = models.CharField(unique=True, max_length=200)
    company_info = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    

class ProductType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    quantity = models.IntegerField()
    type = models.ForeignKey(ProductType,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class BuyerInfo(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(unique=True)
    address = models.TextField()
    contact_no = models.IntegerField()
    company = models.ForeignKey(CompanyInfo,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class SellerInfo(models.Model):
    buyer = models.ForeignKey(BuyerInfo,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    company = models.ForeignKey(CompanyInfo,on_delete=models.CASCADE)

    def __str__(self):
        return self.buyer


class VendorInfo(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(unique=True)
    address = models.TextField()
    contact_no = models.IntegerField()
    company_name = models.CharField(max_length=200)
    company = models.ForeignKey(CompanyInfo,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class PurchaseInfo(models.Model):
    vendor = models.ForeignKey(VendorInfo,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    company = models.ForeignKey(CompanyInfo,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.vendor

