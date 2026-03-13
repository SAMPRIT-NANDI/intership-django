from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import ProductCourseMapping
from product.models import Product
from course.models import Course

class ProductCourseMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCourseMapping
        fields = '__all__'

    def validate(self, data):
        product = data.get('product')
        course = data.get('course')
        if ProductCourseMapping.objects.filter(product=product, course=course).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise ValidationError("This product-course pair already exists.")
        if data.get('primary_mapping'):
            if ProductCourseMapping.objects.filter(product=product, primary_mapping=True).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise ValidationError("Product already has a primary course mapping.")
        return data
