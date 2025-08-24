from django.urls import path
from .views import StudentDashboardViewSet

profile = StudentDashboardViewSet.as_view({'get': 'profile'})
show_result = StudentDashboardViewSet.as_view({'get': 'show_result'})
show_attendance = StudentDashboardViewSet.as_view({'get': 'show_attendance'})

urlpatterns = [
    path('profile/', profile, name='show-details'),
    path('result/', show_result, name='show-result'),
    path('attendance/', show_attendance, name='show-attendance'),
]