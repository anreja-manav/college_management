from django.contrib import admin
from .models import Courses, Semesters, Result
# Register your models here.

admin.site.register(Courses)
admin.site.register(Semesters)
admin.site.register(Result)