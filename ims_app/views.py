from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializer import *
from rest_framework.generics import GenericAPIView

# Create your views here.
# Create your views here.
# @api_view(['GET'])
# def companyInfoApiView(request):
#     company_info_objects = CompanyInfo.objects.all()
#     serializer = CompanyInfoSerializer(company_info_objects,many=True)
#     return Response(serializer.data)

class CompanyInfoApiView(GenericAPIView):
    queryset = CompanyInfo.objects.all()

    def get(self,request):
        company_info_objects = self.get_queryset()
        serializer = CompanyInfoSerializer(company_info_objects,many=True)
        return Response(serializer.data)
