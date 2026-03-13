from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Certification
from .serializers import CertificationSerializer
from course.models import Course

class CertificationListCreateAPIView(APIView):
    def get(self, request):
        queryset = Certification.objects.filter(is_active=True)
        course_id = request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_certification_mappings__course_id=course_id, course_certification_mappings__is_active=True).distinct()
        serializer = CertificationSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CertificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CertificationDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Certification, pk=pk, is_active=True)

    def get(self, request, pk):
        certification = self.get_object(pk)
        serializer = CertificationSerializer(certification)
        return Response(serializer.data)

    def put(self, request, pk):
        certification = self.get_object(pk)
        serializer = CertificationSerializer(certification, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        certification = self.get_object(pk)
        serializer = CertificationSerializer(certification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        certification = self.get_object(pk)
        certification.is_active = False
        certification.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
