from django.db import models
from admins.models import Roles
from acedmics.models import Subjects

# Create your models here.

class Teachers(models.Model):
    role = models.ForeignKey(Roles, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.subject}"

