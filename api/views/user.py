from rest_framework import viewsets,status
from api.serializers.user import ClientProfileSerializer, EmployeeProfileSerializer, UserSerializer, EmergencyContactSerializer
from users.models import ClientProfile, EmployeeProfile, User, EmergencyContact

from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404 
from rest_framework.response import Response

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

@extend_schema(
    tags=['Admin APIs'], summary="Employee Profile"
)
class EmployeeProfileViewsetForAdmin(viewsets.ModelViewSet):
    serializer_class = EmployeeProfileSerializer
    queryset = EmployeeProfile.objects.all()
    permission_classes = [IsAdminUser]

    def get_object(self):
        queryset = self.queryset
        
        qs =  self.filter_queryset(queryset)

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(qs, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def get_serializer_class(self):
        if self.action in ['list_emergency_contacts', 'create_emergency_contact', 'partial_update_emergency_contact']:
            return EmergencyContactSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        if self.action in ['list_emergency_contacts', 'create_emergency_contact', 'partial_update_emergency_contact']:
            employee_profile = self.get_object()                
            return EmergencyContact.objects.filter(employee=employee_profile)

        return super().get_queryset()

    @action(detail=True, methods=['get'], url_path='emergency-contacts-list')
    def list_emergency_contacts(self, request, *args, **kwargs):
        employee_profile = self.get_object()
        emergency_contacts = EmergencyContact.objects.filter(employee=employee_profile)
        serializer = EmergencyContactSerializer(emergency_contacts, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='emergency-contacts/create')
    def create_emergency_contact(self, request, *args, **kwargs):
        employee_profile = self.get_object()
        serializer = EmergencyContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(employee=employee_profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['patch'], url_path='emergency-contacts/(?P<contact_id>[^/.]+)')
    def partial_update_emergency_contact(self, request, *args, **kwargs):
        employee_profile = self.get_object()
        contact_id = kwargs.get("contact_id")
        try:
            emergency_contact = EmergencyContact.objects.get(id=contact_id, employee=employee_profile)
        except EmergencyContact.DoesNotExist:
            return Response({"detail": "Emergency contact not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmergencyContactSerializer(emergency_contact, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=True, methods=['delete'], url_path='emergency-contacts/(?P<contact_id>[^/.]+)')    
    def delete_emergency_contact(self, request, *args, **kwargs):
        employee_profile = self.get_object()
        contact_id = kwargs.get("contact_id")
        try:
            emergency_contact = EmergencyContact.objects.get(id=contact_id, employee=employee_profile)
        except EmergencyContact.DoesNotExist:
            return Response({"detail": "Emergency contact not found."}, status=status.HTTP_404_NOT_FOUND)

        emergency_contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    