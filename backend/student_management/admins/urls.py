from django.urls import path
from .views import AdminViewSet

admin_create = AdminViewSet.as_view({'post': 'create_admin'})
admin_login = AdminViewSet.as_view({'post': 'login'})
admin_list = AdminViewSet.as_view({'get': 'list_admin'})
admin_update = AdminViewSet.as_view({'post': 'update_admin'})
partial_admin_update = AdminViewSet.as_view({'post': 'partial_update_admin'})
admin_delete = AdminViewSet.as_view({'post': 'admin_delete'})

urlpatterns = [
    path('create/', admin_create, name='admin-create'),
    path('login/', admin_login, name='admin-login'),
    path('list/', admin_list, name='admin-list'),
    path('update/', admin_login, name='admin-update'),
    path('partial_update/', admin_login, name='admin-partial-update'),
    path('delete/', admin_login, name='admin-delete'),
]