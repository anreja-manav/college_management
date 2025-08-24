from django.urls import path
from .views import ResultViewSet, CoursesViewSet

add_result = ResultViewSet.as_view({'post': 'add_result'})
update_result = ResultViewSet.as_view({'patch': 'update_result'})
delete_result = ResultViewSet.as_view({'delete': 'delete_result'})
add_course = CoursesViewSet.as_view({'post': 'add_course'})
update_course = CoursesViewSet.as_view({'patch': 'update_course'})
delete_course = CoursesViewSet.as_view({'delete': 'delete_course'})
list_course = CoursesViewSet.as_view({'get': 'list_course'})

urlpatterns = [
    path('add/result/', add_result, name='add-result'),
    path('update/result/', update_result, name='update-result'),
    path('delete/result/', delete_result, name='delete-result'),
    path('add/course/', add_course, name='add-course'),
    path('list/course/', list_course, name='list-course'),
    path('update/course/', update_course, name='update-course'),
    path('delete/course/', delete_course, name='delete-course'),
]
