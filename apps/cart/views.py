from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets

from apps.cart import serializers
from apps.catalogue.models import Product
from apps.cart.models import Basket, Line


class AddCartView(APIView):
    """
    API for add product to cart 

    :param productId: Integer value <br>
    :param quantity: Integer value  <br>
    """
    def post(self, request):
        serializer = serializers.AddCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = request.data.get('productId')
        quantity = request.data.get('quantity')
        product = Product.objects.filter(id=product_id)
        if not product.exists():
            return Response(data={'message': 'Invalid Product'}, status=status.HTTP_400_BAD_REQUEST)
        basket = Basket.objects.filter(owner=request.user, status=Basket.OPEN).first()
        if not basket:
            basket = request.basket
            basket.owner = request.user
            basket.save()
        line = basket.lines.filter(product=product.first()).first()
        if line:
            line.quantity += int(quantity)
            line.save()
        else:
            line = Line(product=product.first(), quantity=int(quantity), basket=basket,
                        price=product.first().actual_price())
            line.save()

        return Response(data={'response': {}, 'error_type': 200, 'status': True,
                              'message': 'Product added to cart successfully'}, status=status.HTTP_200_OK)


class GetCartView(APIView):
    """
    API for listing cart items
    """
    def get(self, request):
        basket = Basket.objects.filter(owner=request.user,status=Basket.OPEN)
        if not basket.exists():
            return Response(data={'response': {},
                                  'message': 'You have not a basket', 'error_type': 201, 'status': False},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.GetCartSerializer(basket, many=True, context={'request': request})
        return Response({'response': {'cartList': serializer.data},
                         'error_type': 200, 'status': True, 'message': 'Cart detail'},
                        status=status.HTTP_200_OK)


class RemoveFromCartView(APIView):
    """
    API for remove product from cart \n

    :param productId: Integer value  <br>
    """
    def post(self, request):
        serializer = serializers.BasketDataSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        productId = serializer.data.get('productId')
        basket = Basket.objects.filter(owner=request.user, status=Basket.OPEN)
        line = basket.first().lines.filter(product__id=productId)
        if not line.exists():
            return Response(data={'response': {}, 'message': 'the product is not in basket', 'error_type': 201,
                                  'status': False},
                            status=status.HTTP_400_BAD_REQUEST)
        line.first().delete()
        return Response({'response': {}, "message": 'Product removed successfully', "error_type": 200, "status": True},
                        status=status.HTTP_200_OK)


class CartItemCountUpdateView(APIView):
    """
    API for updating cart item count \n

    :param productId: integer value <br>
    :param quantity : integer value <br>

    """

    def post(self, request):
        serializer = serializers.AddCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.data.get('productId')
        quantity = serializer.data.get('quantity')
        product = Product.objects.filter(id=product_id)
        if not product.exists():
            return Response(data={'message': 'Invalid Product', 'status': False, 'error_type': 201},
                            status=status.HTTP_400_BAD_REQUEST)
        basket = Basket.objects.filter(owner=request.user, status=Basket.OPEN).first()
        if not basket:
            basket = request.basket
            basket.owner = request.user
            basket.save()
        line = basket.lines.filter(product=product.first()).first()
        if not line:
            return Response(data={'response': {}, 'message': 'the product is not in your basket',
                                  'error_type': 201, 'status': False},
                            status=status.HTTP_400_BAD_REQUEST)
        if line:
            line.quantity = int(quantity)
            line.save()
        else:
            line = Line(product=product.first(), quantity=int(quantity), basket=basket)
            line.save()
        return Response(data={'response': {},
                              'message': 'Cart item count updated successfully', 'error_type': 200, 'status': True},
                        status=status.HTTP_200_OK)


class CartItemVariantUpdateView(APIView):
    """
    API for change cart item variant \n

    :param oldProductId: integer value , existing product id
    :param newProductId: integer value , new product id for update the variant
    :param newQuantity: integer value , new product quantity
    """

    def post(self, request):
        serializer = serializers.ProductVariantUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_product = Product.objects.filter(id=serializer.data.get('oldProductId'))
        new_product = Product.objects.filter(id=serializer.data.get('newProductId'))
        if not old_product.exists() or not new_product.exists():
            return Response(data={'response': {}, 'message': 'invalid product', 'error_type': 201, 'status': False},
                            status=status.HTTP_400_BAD_REQUEST)
        basket = Basket.objects.filter(owner=request.user, status=Basket.OPEN).first()
        if not basket:
            basket = request.basket
            basket.owner = request.user
            basket.save()
            return Response(data={'response': {}, 'message': 'Your basket have not product',
                                  'error_type': 201, 'status': False},
                            status=status.HTTP_400_BAD_REQUEST)
        line = basket.lines.filter(product__id=old_product.first().id)
        if not line.exists():
            return Response(data={'response': {}, 'message': 'The old product id not in basket',
                                  'error_type': 201, 'status': False},
                            status=status.HTTP_400_BAD_REQUEST)
        line.first().delete()
        line = basket.lines.filter(product=new_product.first()).first()
        if line:
            line.quantity = int(serializer.data.get('newQuantity'))
            line.save()
        else:
            line = Line(product=new_product.first(), quantity=int(serializer.data.get('newQuantity')), basket=basket)
            line.save()
        return Response(data={'response': {}, 'message': 'Cart item variant updated successfully',
                              'error_type': 200, 'status': True})

