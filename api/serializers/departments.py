from users.models import Department, Designation, Teams
from rest_framework import serializers

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description']

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ['id', 'name', 'description']

class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = ['id', 'name', 'description', 'department']
        depth = 1
