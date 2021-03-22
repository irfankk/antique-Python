from django.urls import path, include

from rest_framework import routers

from apps.card import views

router = routers.DefaultRouter()


urlpatterns = [

    path(r'', include(router.urls)),
    path(r'add', views.AddCartView.as_view(), name="add-cart")
    path(r'list', views.GetCartView.as_view(), name="list-cart")
    path(r'remove', views.RemoveFromCartView.as_view(), name="remove-cart")

 ]
