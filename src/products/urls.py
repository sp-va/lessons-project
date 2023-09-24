from django.urls import path, include

from rest_framework import routers

from products.views import AllLessonsViewSet, ProductViewSet, LessonViewSet, AllowedProductsViewSet, WatchedLessonsViewSet, CertainProductLessonsViewSet, ProductsStatsViewSet

router = routers.DefaultRouter()


router.register(r'create_product', ProductViewSet, basename='create_product')
router.register(r'create_lesson', LessonViewSet, basename='create_lesson')
router.register(r'allowed_products', AllowedProductsViewSet, basename='allowed_products')
router.register(r'watched_lessons', WatchedLessonsViewSet, basename='watched_lessons')
router.register(r'all_lessons', AllLessonsViewSet)
router.register(r'certain_product_lessons', CertainProductLessonsViewSet)
router.register(r'all_products', ProductsStatsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]