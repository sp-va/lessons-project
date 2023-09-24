from rest_framework import serializers
from django.db.models import Count, Sum

from products.models import *

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'owner']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class AllowedProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllowedProducts
        fields = '__all__'

class WatchedLessonsSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()

    def get_is_completed(self, object):
        return object.is_completed()

    class Meta:
        model = WatchedLessons
        fields = ['lesson', 'watcher', 'time_watched', 'is_completed']

class CertainProductWatchedLessonsSerializer(WatchedLessonsSerializer):
    class Meta:
        model = WatchedLessons
        fields = ['lesson', 'watcher', 'time_watched', 'is_completed', 'last_watch_date']

class AllProductsStatsSerializer(serializers.ModelSerializer):
    general_watch_counter = serializers.SerializerMethodField()
    general_time_watched = serializers.SerializerMethodField()
    product_students_counter = serializers.SerializerMethodField()
    purchase_percentage = serializers.SerializerMethodField()

    def get_general_watch_counter(self, object):
        queryset = WatchedLessons.objects.values('lesson_id', 'watcher_id').annotate(count=Count('id'))
        unique_watches_count = queryset.filter(count=1).count()
        return unique_watches_count
        
    def get_general_time_watched(self, object):
        total_time = WatchedLessons.objects.filter(lesson__related_product=object).aggregate(sum=Sum('time_watched'))
        return total_time['sum']
       
    def get_product_students_counter(self, object):
        students_count = AllowedProducts.objects.filter(products_id=object).count()
        return students_count
    
    def get_purchase_percentage(self, object):
        platform_users_count = MyUser.objects.count()
        students_count = AllowedProducts.objects.filter(products_id=object).count()
        percentage = (students_count / platform_users_count) * 100
        return percentage

    class Meta:
        model = Product
        fields = ['id', 'owner', 'general_watch_counter', 'general_time_watched', 'product_students_counter', 'purchase_percentage',]
