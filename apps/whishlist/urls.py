from django.urls import path, include

from rest_framework import routers

from apps.whishlist import views

router = routers.DefaultRouter()
router.register(r'list', views.WishListView, basename='whishlist-list')
router.register(r'add', views.AddWishListView, basename='whishlist-add')


urlpatterns = [

    path(r'', include(router.urls)),
    path(r'delete', views.RemoveWhilshlist.as_view(), name="delete-whishlist")

 ]
