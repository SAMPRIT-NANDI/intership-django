from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Course
from .serializers import CourseSerializer
from product.models import Product

class CourseListCreateAPIView(APIView):
    def get(self, request):
        queryset = Course.objects.filter(is_active=True)
        product_id = request.query_params.get('product_id')
        if product_id:
            queryset = queryset.filter(product_course_mappings__product_id=product_id, product_course_mappings__is_active=True).distinct()
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Course, pk=pk, is_active=True)

    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = self.get_object(pk)
        course.is_active = False
        course.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
