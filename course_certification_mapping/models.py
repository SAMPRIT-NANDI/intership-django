from django.db import models
from course.models import Course
from certification.models import Certification

class CourseCertificationMapping(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_certification_mappings')
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE, related_name='course_certification_mappings')
    primary_mapping = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'course_certification_mapping'
        unique_together = ['course', 'certification']

    def __str__(self):
        return f"{self.course.name} - {self.certification.name}"
