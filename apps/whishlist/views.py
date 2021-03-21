from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.account.models import User
from apps.catalogue.models import Product
from apps.wishlist.models import Line, Wishlist
from apps.wishlist.serializers import WishListSerializer, AddWishListSerializer, RemoveWishlistSerializer
from apps.apiv1.home.utils import percentage
from apps.apiv1.localeprice import localeprice, get_current_currency
from apps.apiv1.currency.serializers import CurrencySerializer


class AddWishListView(viewsets.ModelViewSet):
    """
    API for adding product to wish list

    :param productId: integer value
    :param userId: integer value
    """

    http_method_names = ['post']
    queryset = Line.objects.all()
    serializer_class = AddWishListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = request.data['userId']
        product_id = request.data['productId']
        user = request.user
        try:
            product = Product.objects.get(id=product_id)
        except:
            return Response(data={'response':{}, 'message': 'Product id is not exist',
                                  'error_type': 201, 'status': False},
                            status=status.HTTP_400_BAD_REQUEST)

        wish_list, created = Wishlist.objects.get_or_create(user=user)
        if Line.objects.filter(wishlist=wish_list, product=product):
            Line.objects.get(wishlist=wish_list, product=product).delete()
            return Response(data={'response': {}, "message": "Removed from Wish List",
                                  "error_type": "200", "status": True},
                            status=status.HTTP_200_OK)
        else:
            line = Line.objects.create(wishlist=wish_list, product=product)
            return Response(data={'response': {},
                                  "message": "Added to WishList successfully", "error_type": "200", "status": True},
                            status=status.HTTP_200_OK)


class WishListView(viewsets.ModelViewSet):
    """
    API for showing wish list items

    :param id: integer value
    """
    http_method_names = ['post']
    queryset = User.objects.all()
    serializer_class = WishListSerializer

    def create(self, request, *args, **kwargs):
        current_currency = get_current_currency(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        wish_list, created = Wishlist.objects.get_or_create(user=user)
        if not wish_list.lines.all():
            return Response(data={'response': {}, "message": "No Records found", "error_type": "201", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)
        wish_list = []
        for product in user.wishlist.lines.all():
            product_id = product.product.id
            description = product.product.description
            price = product.product.price
            image_url = None
            for image in product.product.images.all():
                if image.original:
                    image_url = image.original.url
            if product.product.title:
                name = product.product.title
            else:
                name = Product.objects.get(id=product.product.parent_id).title
            product_data = {'productId': product_id,
                            'productName': name,
                            'productImageUrl': image_url,
                            'productDescription': description,
                            'productStock': product.product.stock,
                            }
            wish_list.append(product_data)
        if wish_list:
            return Response(data={'response': {"wishList": wish_list},
                                  'message': 'wish list items', 'error_type': 200, 'status': True},
                            status=status.HTTP_200_OK)
        else:
            return Response(data={'response': {}, "message": "No Records found",
                                  "error_type": "201", "status": False},
                            status=status.HTTP_400_BAD_REQUEST)


class RemoveWhilshlist(APIView):
    """
    API for removing product from wish list

    :param productId: integer value
    :param userId: integer value
    """
    def post(self, request):
        serializer = RemoveWishlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = Product.objects.filter(id=request.data['productId'])
        if not product.exists():
            return Response(data={'response': {}, "message": "Product id is not valid",
                                  "error_type": 201, "status": False},
                            status=status.HTTP_400_BAD_REQUEST)

        wish_list, created = Wishlist.objects.get_or_create(user=request.user)
        if Line.objects.filter(wishlist=wish_list, product=product.first()).exists():
            Line.objects.get(wishlist=wish_list, product=product.first()).delete()
            return Response(data={'response': {},
                                  "message": "Product removed successfully","error_type": 200,"status": True},
                            status=status.HTTP_200_OK)

        return Response(data={'response': {}, "message": "Sorry Please try again", "error_type": 201, "status": False},
                        status=status.HTTP_400_BAD_REQUEST)