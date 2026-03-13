from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import ProductCourseMapping
from .serializers import ProductCourseMappingSerializer

class ProductCourseMappingListCreateAPIView(APIView):
    def get(self, request):
        queryset = ProductCourseMapping.objects.filter(is_active=True)
        product_id = request.query_params.get('product_id')
        course_id = request.query_params.get('course_id')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        serializer = ProductCourseMappingSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductCourseMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductCourseMappingDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(ProductCourseMapping, pk=pk, is_active=True)

    def get(self, request, pk):
        mapping = self.get_object(pk)
        serializer = ProductCourseMappingSerializer(mapping)
        return Response(serializer.data)

    def put(self, request, pk):
        mapping = self.get_object(pk)
        serializer = ProductCourseMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        mapping = self.get_object(pk)
        serializer = ProductCourseMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        mapping = self.get_object(pk)
        mapping.is_active = False
        mapping.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
