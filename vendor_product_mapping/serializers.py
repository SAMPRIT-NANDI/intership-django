from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import VendorProductMapping
from vendor.models import Vendor
from product.models import Product

class VendorProductMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProductMapping
        fields = '__all__'

    def validate(self, data):
        vendor = data.get('vendor')
        product = data.get('product')
        if VendorProductMapping.objects.filter(vendor=vendor, product=product).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise ValidationError("This vendor-product pair already exists.")
        if data.get('primary_mapping'):
            if VendorProductMapping.objects.filter(vendor=vendor, primary_mapping=True).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise ValidationError("Vendor already has a primary product mapping.")
        return data
