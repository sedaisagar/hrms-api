from rest_framework import viewsets
from users.models import Department, Designation, Teams
from api.serializers.departments import DepartmentSerializer, DesignationSerializer, TeamsSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAdminUser

@extend_schema(tags=['Departments'])
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminUser]

@extend_schema(tags=['Designations'])
class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    permission_classes = [IsAdminUser]

@extend_schema(tags=['Teams'])
class TeamsViewSet(viewsets.ModelViewSet):
    queryset = Teams.objects.all()
    serializer_class = TeamsSerializer
    permission_classes = [IsAdminUser]

