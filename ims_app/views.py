from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import *
from .serializer import *
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from .permissions import CustomModelPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Create your views here.
# @api_view(['GET'])
# def companyInfoApiView(request):
#     company_info_objects = CompanyInfo.objects.all()
#     serializer = CompanyInfoSerializer(company_info_objects,many=True)
#     return Response(serializer.data)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(username=email,password=password)
    if user == None:
        return Response('User not found!')
    else:
        token,_ = Token.objects.get_or_create(user=user)
        return Response({'token':token.key})
    
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def register(request):
    password = request.data.get('password')
    group_id = request.data.get('group')
    try:
        group_object = Group.objects.get(id=group_id)
    except:
        return Response({'error':'No such groups!'})
    hash_password = make_password(password)
    request.data['password'] = hash_password
    request.data['company_info'] = request.user.company_info.id
    serializer = UserInfoSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.groups.add(group_object.id)
        user.save()
        return Response({'data':'User created!'})
    else:
        return Response({'error':serializer.errors})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def admin_create(request):
    password = request.data.get('password')
    try:
        group_object = Group.objects.get(name='Admin')
    except:
        return Response({'error':'No such groups!'})
    hash_password = make_password(password)
    request.data['password'] = hash_password
    serializer = UserInfoSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.groups.add(group_object.id)
        user.save()
        return Response({'data':'Admin created!'})
    else:
        return Response({'error':serializer.errors})

class CompanyInfoApiView(GenericAPIView):
    queryset_model = CompanyInfo
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    # filterset_fields = ['address']
    search_fields = ['address','name']
    permission_classes = [IsAuthenticated,CustomModelPermission]

    def get(self,request):
        company_info_objects = self.get_queryset()
        filter_objects = self.filter_queryset(company_info_objects)
        serializer = CompanyInfoSerializer(filter_objects,many=True)
        return Response({'data':serializer.data})
    
    def post(self,request):
        serializer = CompanyInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':'Data created!'})
        else:
            return Response({'error':serializer.errors})
        
class CompanyInfoIdApiView(GenericAPIView):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    permission_classes = [IsAuthenticated,CustomModelPermission]

    def get(self,request,pk):
        try:
            company_info_object = CompanyInfo.objects.get(id=pk)
        except:
            return Response('Data not found!')
        serializer = CompanyInfoSerializer(company_info_object)
        return Response(serializer.data)
    
    def put(self,request,pk):
        try:
            company_info_object = CompanyInfo.objects.get(id=pk)
        except:
            return Response('Data not found!')
        serializer = CompanyInfoSerializer(company_info_object,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Data updated successfully')
        else:
            return Response(serializer.errors)
        
    def delete(self,request,pk):
        try:
            company_info_object = CompanyInfo.objects.get(id=pk)
        except:
            return Response('Data not found!')
        company_info_object.delete()
        return Response('Data deleted successfully!')

class GroupApiView(GenericAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get(self,request):
        group_objects = self.get_queryset()
        serializer = self.serializer_class(group_objects,many=True)
        return Response({'data':serializer.data})
        

class ProductTypeApiView(GenericAPIView):
    queryset_model = ProductType
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    # permission_classes = [IsAuthenticated,CustomModelPermission]

    def post(self, request):
        serializer = ProductTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':'data created.'})
        else:
            return Response({'error':'serializer.errors'})
        
    def get(self, request):
        product_type_objects = self.get_queryset()
        filter_object = self.filter_queryset(product_type_objects)
        serializer = ProductTypeSerializer(filter_object,many=True)
        return Response({'data':serializer.data})

class ProductTypeIdApiView(GenericAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer

    def get(self, request,pk):
        try:
            product_type_objects = ProductType.objects.get(id=pk)
        except:
            return Response('Data not found!')
        serializer = ProductsSerializer(product_type_objects)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            product_type_objects = ProductType.objects.get(id=pk)
        except:
            return Response('data not found!')
        serializer = ProductsSerializer(product_type_objects,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('data updated successfully!')
        else:
            return Response(serializer.errors)
        
    def delete(self,request, pk):
        try:
            product_type_objects = ProductType.objects.get(id=pk)
        except:
            return Response('Data not found!')
        product_type_objects.delete()
        return Response('data deleted successfully!')
    


    
class ProductsApiView(GenericAPIView):
    queryset_model = Product
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]

    def post(self,request):
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':'data Created.'})
        else:
            return Response({'error':serializer.errors})
    
    def get(self,request):
        products_objects = self.get_queryset()
        filter_objects = self.filter_queryset(products_objects)
        serializer = ProductsSerializer(filter_objects,many=True)
        return Response({'data':serializer.data})
    
        
    
class ProductInfoIdApiView(GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
    # permission_classes = [IsAuthenticated,CustomModelPermission]

    def get(self,request,pk):
        try:
            product_info_object = Product.objects.get(id=pk)
        except:
            return Response('Data not found!')
        serializer = ProductsSerializer(product_info_object)
        return Response(serializer.data)
    
    def put(self,request,pk):
        try:
            product_info_object = Product.objects.get(id=pk)
        except:
            return Response('Data not found!')
        serializer = ProductsSerializer(product_info_object,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Data updated successfully')
        else:
            return Response(serializer.errors)
        
    def delete(self,request,pk):
        try:
            product_info_object = Product.objects.get(id=pk)
        except:
            return Response('Data not found!')
        product_info_object.delete()
        return Response('Data deleted successfully!')


class BuyerInfoApiView(GenericAPIView):
    queryset = BuyerInfo.objects.all()
    serializer_class = BuyerInfoSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]

    def post(self,request):
        serializer = BuyerInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':'Buyer Created.'})
        else:
            return Response({'error':serializer.errors})
        
    def get(self, request):
        buyer_info_objects = self.get_queryset()
        filter_object = self.filter_queryset(buyer_info_objects)
        serializer = BuyerInfoSerializer(filter_object, many=True)
        return Response({'data':serializer.data})
    
class BuyerInfoIdApiView(GenericAPIView):
    queryset = BuyerInfo.objects.all()
    serializer_class = BuyerInfoSerializer

    def get(self,request,pk):
        try:
            buyer_info_objects = BuyerInfo.objects.get(id=pk)
        except:
            return Response('data not found!')
        serializer = BuyerInfoSerializer(buyer_info_objects)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            buyer_info_objects = BuyerInfo.objects.get(id=pk)
        except:
            return Response('data not found!')
        serializer = BuyerInfoSerializer(buyer_info_objects,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('data update successfully!')
        else:
            return Response(serializer.errors)
        
    def delete(self,request,pk):
        try:
            buyer_info_objects = BuyerInfo.objects.get(id=pk)
        except:
            return Response('data not found!')
        buyer_info_objects.delete()
        return Response('data deleted successfully!')
    

class SellerInfoApiView(GenericAPIView):
    queryset_model = SellerInfo
    queryset = SellerInfo.objects.all()
    serializer_class = SellerInfoSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]

    def post(self, request):
        serializer = SellerInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':'Data Created.'})
        else:
            return Response({'data':serializer.errors})
        
    def get(self, request):
        seller_info_objects = self.get_queryset()
        filter_objects = self.filter_queryset(seller_info_objects)
        serializer = SellerInfoSerializer(filter_objects,maney=True)
        return Response({'data':serializer.data})
    

class SellerInfoIdApiView(GenericAPIView):
    queryset = SellerInfo.objects.all()
    serializer_class = SellerInfoSerializer

    def get(self,request,pk):
        try:
            seller_info_objects = SellerInfo.objects.get(id=pk)
        except:
            return Response('data no found!')
        serializer = SellerInfoSerializer(seller_info_objects)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            seller_info_objects = SellerInfo.objects.get(id=pk)
        except:
            return Response('data not found!')
        serializer = SellerInfoSerializer(seller_info_objects,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('data update successfully!')
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        try:
            seller_info_objects = SellerInfo.objects.get(id=pk)
        except:
            return Response('data not found!')
        seller_info_objects.delete()
        return Response('data deleted successfully!')

    

class VendorInfoApiView(GenericAPIView):
    queryset_model = VendorInfo
    queryset = VendorInfo.objects.all()
    serializer_class = VenderInfoSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]

    def post(self, request):
        serializer = VenderInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':'data created!'})
        else:
            return Response({'erroe':serializer.errors})
        
    def get(self,request):
        vendor_info_object = self.get_queryset()
        filter_objects = self.filter_queryset(vendor_info_object)
        serializer = VenderInfoSerializer(filter_objects,many=True)
        return Response({'data':serializer.data})
    

class VendorInfoIdApiView(GenericAPIView):
    queryset = VendorInfo.objects.all()
    serializer_class = VenderInfoSerializer

    def get(self, request, pk):
        try:
            vendor_info_objects = VendorInfo.objects.get(id=pk)
        except:
            return Response('data not found!')
        serializer = VenderInfoSerializer(vendor_info_objects)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            vendor_info_objects = VendorInfo.objects.get(id=pk)
        except:
            return Response('data not found!')
        serializer = VenderInfoSerializer(vendor_info_objects,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('data update successfully')
        else:
            return Response(serializer.errors)
        
    def delete(self, request,pk):
        try:
            vendor_info_objects = VendorInfo.objects.get(id=pk)
        except:
            return Response('data not found!')
        vendor_info_objects.delete()
        return Response('data deleted successfully!')        


class PurchaseInfoApiView(GenericAPIView):
    queryset_model = PurchaseInfo
    queryset = PurchaseInfo.objects.all()
    serializer_class = PurchaseInfoSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]

    def post(self,request):
        serializer = PurchaseInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':'data created!'})
        else:
            return Response({'error':serializer.errors})
        
    def get(self,request):
        purchase_info_objects = self.get_queryset()
        filter_objects = self.filter_queryset(purchase_info_objects)
        serializer = PurchaseInfoSerializer(filter_objects, many=True)
        return Response({'data':serializer.data})
    

class PurchaseInfoIdApiView(GenericAPIView):
    serializer_class = PurchaseInfoSerializer
    queryset = PurchaseInfo.objects.all()

    def get(self, request, pk):
        try:
            purchase_info_objects = PurchaseInfo.objects.get(id=pk)
        except:
            return Response('data not found!')
        serializer = PurchaseInfoSerializer(purchase_info_objects)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            purchase_info_objects = PurchaseInfo.objects.get(id=pk)
        except:
            return Response('data not found!')
        serializer = PurchaseInfoSerializer(purchase_info_objects,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('data update successfully!')
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        try:
            purchase_info_objects = PurchaseInfo.objects.get(id=pk)
        except:
            return Response('data not found!')
        purchase_info_objects.delete()
        return Response('data deleted successfully!')




