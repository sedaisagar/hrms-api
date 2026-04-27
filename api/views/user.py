from rest_framework import viewsets
from api.serializers.user import ClientProfileSerializer, UserSerializer
from users.models import ClientProfile, User

from rest_framework.permissions import IsAdminUser

from drf_spectacular.utils import extend_schema

@extend_schema(
    tags=['Admin APIs'],
)
class UserViewSetForAdmin(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    http_method_names = [
        'get', 
        # 'post', 
        # 'put', 
        'patch', 
        # 'delete'
    ]

@extend_schema(
    tags=['Admin APIs'], summary="Client Profile"
)
class ClientProfileViewsetForAdmin(viewsets.ModelViewSet):
    serializer_class = ClientProfileSerializer
    queryset = ClientProfile.objects.all()
    permission_classes = [IsAdminUser]
