from django.db import models

# Create your models here.

class Class(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Students(models.Model):
    name = models.CharField(max_length=100)
    s_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    age = models.IntegerField()
    roll_no = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.s_class.name} (Roll No: {self.roll_no})"