from rest_framework import serializers
from .models import Vendor
from django.core.exceptions import ValidationError

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

    def validate_code(self, value):
        if Vendor.objects.filter(code__iexact=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("Code must be unique.")
        return value
