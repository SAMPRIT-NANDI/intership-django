from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import CourseCertificationMapping
from .serializers import CourseCertificationMappingSerializer

class CourseCertificationMappingListCreateAPIView(APIView):
    def get(self, request):
        queryset = CourseCertificationMapping.objects.filter(is_active=True)
        course_id = request.query_params.get('course_id')
        certification_id = request.query_params.get('certification_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if certification_id:
            queryset = queryset.filter(certification_id=certification_id)
        serializer = CourseCertificationMappingSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseCertificationMappingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseCertificationMappingDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(CourseCertificationMapping, pk=pk, is_active=True)

    def get(self, request, pk):
        mapping = self.get_object(pk)
        serializer = CourseCertificationMappingSerializer(mapping)
        return Response(serializer.data)

    def put(self, request, pk):
        mapping = self.get_object(pk)
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        mapping = self.get_object(pk)
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        mapping = self.get_object(pk)
        mapping.is_active = False
        mapping.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
