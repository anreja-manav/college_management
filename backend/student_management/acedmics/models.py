from django.db import models

# Create your models here.
class Courses(models.Model):
    course_name = models.CharField(max_length=50)

    def __str__(self):
        return self.course_name
    
class Semesters(models.Model):
    SEMESTER_CHOICES = (
        ('1st', 'I'),
        ('2nd', 'II'),
        ('3rd', 'III'),
        ('4th', 'IV'),
        ('5th', 'V'),
        ('6th', 'VI'),
        ('7th', 'VII'),
        ('8th', 'VIII'),
    )

    semester = models.CharField(max_length=5, choices=SEMESTER_CHOICES, unique=True)

    def __str__(self):
        return self.semester

class Result(models.Model):
    EXAM_CHOICE = (
        ('semester', 'Semester'),
        ('sessional', 'Sessional'),
        ('re-appear', 'Re-Appear'),
        ('reval', 'Reval'),
    )
    student = models.ForeignKey("accounts.StudentProfile", on_delete=models.CASCADE, related_name='results')
    semester = models.ForeignKey(Semesters, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=15, choices=EXAM_CHOICE)
    subjects = models.JSONField(default=dict)

    final_status = models.CharField(max_length=20, default="Pending")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "semester", "exam_type")

    def total_marks(self):
        if self.final_status == "Pass":
            return sum(sub.get("marks", 0) for sub in self.subjects.values())
        return None

    def max_total(self):
        return sum(sub.get("max_marks", 0) for sub in self.subjects.values())

    def percentage(self):
        if self.final_status == "Pass":
            max_total = self.max_total()
            return (self.total_marks() / max_total) * 100 if max_total else 0
        return None

    def compute_final_status(self, pass_mark=33):
        failed_subjects = [
            sub for sub, data in self.subjects.items()
            if data.get("marks", 0) < pass_mark
        ]
        self.final_status = "Fail" if failed_subjects else "Pass"
        return self.final_status

    def save(self, *args, **kwargs):
        self.compute_final_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.semester} - {self.exam_type} - {self.final_status}"
    
    
    
    