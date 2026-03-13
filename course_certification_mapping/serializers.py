from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import CourseCertificationMapping
from course.models import Course
from certification.models import Certification

class CourseCertificationMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCertificationMapping
        fields = '__all__'

    def validate(self, data):
        course = data.get('course')
        certification = data.get('certification')
        if CourseCertificationMapping.objects.filter(course=course, certification=certification).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise ValidationError("This course-certification pair already exists.")
        if data.get('primary_mapping'):
            if CourseCertificationMapping.objects.filter(course=course, primary_mapping=True).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise ValidationError("Course already has a primary certification mapping.")
        return data
