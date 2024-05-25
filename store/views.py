from django.shortcuts import render

from store.models import Category, Product, Gallery, Specification, Size,\
      Color, Cart, CartOrder, CartOrderItem, ProductFaq, Review, WhishList,\
          Notification, Coupon
from store.serializers import ProductSerializer, CategorySerializer

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        slug = self.kwargs['slug']
        return Product.objects.get(slug=slug)
