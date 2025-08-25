from django.urls import path
from .views import AdminViewSet, DashboardViewSet

login = AdminViewSet.as_view({'post': 'login'})
profile = DashboardViewSet.as_view({'get': 'profile'})

admin_create = AdminViewSet.as_view({'post': 'create_admin'})
admin_list = AdminViewSet.as_view({'get': 'list_admin'})
admin_update = AdminViewSet.as_view({'put': 'update_admin'})
partial_admin_update = AdminViewSet.as_view({'patch': 'partial_update_admin'})
admin_delete = AdminViewSet.as_view({'delete': 'delete_admin'})

teacher_create = AdminViewSet.as_view({'post': 'create_teacher'})
teacher_list = AdminViewSet.as_view({'get': 'list_teacher'})
teacher_update = AdminViewSet.as_view({'put': 'update_teacher'})
partial_teacher_update = AdminViewSet.as_view({'patch': 'partial_update_teacher'})
teacher_delete = AdminViewSet.as_view({'delete': 'delete_teacher'})

student_create = AdminViewSet.as_view({'post': 'create_student'})
student_list = AdminViewSet.as_view({'get': 'list_student'})
student_update = AdminViewSet.as_view({'put': 'update_student'})
partial_student_update = AdminViewSet.as_view({'patch': 'partial_update_student'})
student_delete = AdminViewSet.as_view({'delete': 'delete_student'})

view_attendance = AdminViewSet.as_view({'get': 'view_attendance'})



urlpatterns = [
    path('login/', login, name='login'),
    path('profile/', profile, name='profile'),

    path('create/admin/', admin_create, name='admin-create'),
    path('list/admin/', admin_list, name='admin-list'),
    path('update/admin/', admin_update, name='admin-update'),
    path('partial_update/admin/', partial_admin_update, name='admin-partial-update'),
    path('delete/admin/', admin_delete, name='admin-delete'),

    path('create/teacher/', teacher_create, name='teacher-create'),
    path('list/teacher/', teacher_list, name='teacher-list'),
    path('update/teacher/', teacher_update, name='teacher-update'),
    path('partial_update/teacher/', partial_teacher_update, name='teacher-partial-update'),
    path('delete/teacher/', teacher_delete, name='teacher-delete'),

    path('create/student/', student_create, name='student-create'),
    path('list/student/', student_list, name='student-list'),
    path('update/student/', student_update, name='student-update'),
    path('partial_update/student/', partial_student_update, name='student-partial-update'),
    path('delete/student/', student_delete, name='student-delete'),

    
]