from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.catalogue.models import Product
from apps.catalogue.serializers import ProductListSerializer


class ProductListView(viewsets.ModelViewSet):
	permission_classes = (AllowAny,)
	http_method_names = ['get']
	queryset = Product.objects.filter(status=Product.ACTIVE, stock__gt =0)
	serializer_class = ProductListSerializer