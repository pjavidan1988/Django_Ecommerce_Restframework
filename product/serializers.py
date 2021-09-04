from django.db.models import fields
from rest_framework import serializers
from .models import Category, Product, Picture

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model =Product
        fields = (
            "id",
            "title",
            "keywords",
            "brand_name",
            "model_name",
            "short_description",
            "description",
            "image",
            "slider_image",
            "price",
            "amount",
            "minAmount",
            "detail",
            "transportation",
            "slug",
            "status",
            "get_absolute_url",
            "image_tag",
        )