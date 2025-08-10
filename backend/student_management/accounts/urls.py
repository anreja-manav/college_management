from django.urls import path
from .views import AccountViewSet

admin_create = AccountViewSet.as_view({'post': 'create_admin'})
admin_login = AccountViewSet.as_view({'post': 'login'})
admin_list = AccountViewSet.as_view({'get': 'list_admin'})
admin_update = AccountViewSet.as_view({'put': 'update_admin'})
partial_admin_update = AccountViewSet.as_view({'patch': 'partial_update_admin'})
admin_delete = AccountViewSet.as_view({'delete': 'delete_admin'})

urlpatterns = [
    path('create/', admin_create, name='admin-create'),
    path('login/', admin_login, name='admin-login'),
    path('list/', admin_list, name='admin-list'),
    path('<int:pk>/update/', admin_update, name='admin-update'),
    path('<int:pk>/partial_update/', partial_admin_update, name='admin-partial-update'),
    path('<int:pk>/delete/', admin_delete, name='admin-delete')
]