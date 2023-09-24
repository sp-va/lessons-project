from django.shortcuts import render

from django.shortcuts import render, get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny

from products.serializers import *
from products.models import *

class ProductViewSet(ViewSet):
    queryset = Product.objects.all()

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        object = get_object_or_404(Product, pk=pk)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class LessonViewSet(ViewSet):
    queryset = Lesson.objects.all()

    def create(self, request):
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AllowedProductsViewSet(ViewSet):
    queryset = AllowedProducts.objects.all()

    def create(self, request):
        serializer = AllowedProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WatchedLessonsViewSet(ViewSet):
    queryset = WatchedLessons.objects.all()
    
    def create(self, request):
        serializer = WatchedLessonsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllLessonsViewSet(ViewSet):
    queryset = Lesson.objects.all()

    def list(self, request):
        user_id = request.user.id
        allowed_products = AllowedProducts.objects.filter(user=user_id)
        products = Product.objects.filter(id__in=allowed_products)
        lessons = Lesson.objects.filter(related_product__in=products)
        watched_lessons = WatchedLessons.objects.filter(lesson__in=lessons)
        serialized = WatchedLessonsSerializer(watched_lessons, many=True)
        return Response(serialized.data)

class CertainProductLessonsViewSet(ViewSet):
    queryset = Lesson.objects.all()

    def retrieve(self, request, pk=None):
        user_id = request.user.id
        allowed_products = AllowedProducts.objects.filter(user=user_id)
        products = Product.objects.filter(id__in=allowed_products)
        lessons = Lesson.objects.filter(related_product__in=products, related_product=pk)
        watched_lessons = WatchedLessons.objects.filter(lesson__in=lessons)
        serialized = CertainProductWatchedLessonsSerializer(watched_lessons, many=True)
        return Response(serialized.data)


class ProductsStatsViewSet(ViewSet):
    queryset = Product.objects.all()

    def list(self, request):
        serialized = AllProductsStatsSerializer(self.queryset, many=True)
        return Response(serialized.data)
