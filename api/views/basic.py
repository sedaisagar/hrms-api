from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status

from api.serializers.basic import UserRegistrationSerializer
from users.models import User
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.utils import extend_schema

@extend_schema(
    tags=["Public"], summary="Client User Registration Api"
)
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = []
    authentication_classes = []

    def get_serializer_context(self):
        data =  super().get_serializer_context()
        data.update(
            role="user",
        )
        return data

@extend_schema(
    tags=["Public"], summary="Employee User Registration Api"
)
class EmployeeRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = []
    authentication_classes = []

    def get_serializer_context(self):
        data =  super().get_serializer_context()
        data.update(
            role="employee",
        )
        return data
  
@extend_schema(
    tags=["Public"],
)
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

@extend_schema(
    tags=["Public"],
)
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

@extend_schema(
    tags=["Auth User"],
)
class GetMyProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user : User = request.user
        serializer = UserRegistrationSerializer(user)
        profile_serializer = None

        if user.role == "user":
            try:
                profile = user.client_profile
                from api.serializers.user import ClientProfileSerializer
                profile_serializer = ClientProfileSerializer(profile)
            except:
                profile_serializer = None
        elif user.role == "employee":
            try:
                profile = user.employee_profile
                from api.serializers.user import EmployeeProfileSerializer
                profile_serializer = EmployeeProfileSerializer(profile)
            except:
                profile_serializer = None

        data = {
            "user": serializer.data,
            "profile": profile_serializer.data if profile_serializer else None,
        }
        return Response(data)