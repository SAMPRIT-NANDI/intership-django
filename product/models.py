from django.db import models
from django.core.validators import RegexValidator
from vendor.models import Vendor

class Product(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True, validators=[RegexValidator(r'^[A-Z0-9_-]+$', 'Code must be alphanumeric with -_')])
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return self.name
