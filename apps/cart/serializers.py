from rest_framework import serializers

from apps.basket.models import Basket
from apps.catalogue.models import Product
from apps.apiv1.basket.utils import product_variants
from apps.apiv1.localeprice import localeprice, get_current_currency
from apps.apiv1.currency.serializers import CurrencySerializer


class AddCartSerializer(serializers.Serializer):
    productId = serializers.IntegerField()
    quantity = serializers.IntegerField()


class GetCartSerializer(serializers.ModelSerializer):
    cartId = serializers.SerializerMethodField()
    totalAmount = serializers.SerializerMethodField()
    cartListItem = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()

    def get_cartId(self, obj):
        return obj.id

    def get_cartListItem(self, obj):
        list = []
        current_currency = get_current_currency(self.context["request"])
        for item in obj.lines.all():
            dict_product = {}
            dict_product['productId'] = item.product.id
            dict_product['productName'] = item.product.get_title()
            if item.product.main_image() and item.product.main_image().original:
                dict_product['productImage'] = item.product.main_image().original.url
            else:
                dict_product['productImage'] = None
            dict_product['productVariant'] = item.product.get_all_attributes
            dict_product['productQty'] = item.quantity
            dict_product['productStock'] = item.product.stock
            dict_product['productPrice'] = localeprice(item.price, current_currency)
            dict_product['isOutOfStock'] = 1 if item.product.out_of_stock() else 0
            dict_product['availableVariants'] = product_variants(item.product)

            image = [img.original.url for img in item.product.images.all() if img.original]
            if image:
                dict_product['productImage'] = image[0]
            list.append(dict_product)
        return list

    def get_totalAmount(self, obj):
        current_currency = get_current_currency(self.context["request"])
        return localeprice(obj.get_total(), current_currency)

    def get_currency(self, obj):
        current_currency = get_current_currency(self.context["request"])
        return CurrencySerializer(instance=current_currency, context=self.context).data

    class Meta:
        model = Basket
        fields = ("cartId", 'totalAmount', 'cartListItem', 'currency')


class BasketDataSerializer(serializers.Serializer):
    productId = serializers.IntegerField()

    # def validate_productId(self, productId):
    #     if not Product.objects.filter(id=productId).exists():
    #         raise serializers.ValidationError('Please enter valid product')
    #     request = self.context.get('request')
    #     basket = Basket.objects.filter(owner=request.user, status=Basket.OPEN)
    #     if not basket.exists():
    #         raise serializers.ValidationError('You have not a basket')
    #     line_obj = basket.first().lines.filter(product__id=productId)
    #     if not line_obj.exists():
    #         raise serializers.ValidationError('The product is not in Basket')
    #     return productId


class ProductVariantUpdateSerializer(serializers.Serializer):
    oldProductId = serializers.IntegerField()
    newProductId = serializers.IntegerField()
    newQuantity = serializers.IntegerField()

