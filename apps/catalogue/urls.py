from django.urls import path, include

from rest_framework import routers

from apps.catalogue import views

router = routers.DefaultRouter()
router.register(r'list', views.ProductListView, basename='product-list')


urlpatterns = [

    path(r'', include(router.urls)),

 ]
