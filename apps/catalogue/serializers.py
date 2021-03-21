from rest_framework import serializers, exceptions

from apps.catalogue.models import Product


class ProductListSerializer(serializers.ModelSerializer):

	class Meta:
		model = Product
		fields = ('title', 'status', 'stock', 'price', 'age', 'image', 'description')
