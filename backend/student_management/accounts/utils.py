from rest_framework.response import Response
from rest_framework import status

def is_admin(user):
    if not user.is_authenticated or getattr(user.role, 'role', None) != 'admin':
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
    return None

