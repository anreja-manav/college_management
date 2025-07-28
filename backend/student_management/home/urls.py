from django.urls import path
from .views import StudentAPI

urlpatterns = [
    path('', StudentAPI.as_view()),
]