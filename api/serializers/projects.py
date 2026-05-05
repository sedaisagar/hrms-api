from rest_framework import serializers

from api.serializers.user import ClientProfileSerializer, EmployeeProfileSerializer, UserSerializer
from projects.models import Project, ProjectDocument, ProjectTags, ProjectTask

class ProjectTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTags
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = "__all__"

    def to_representation(self, instance:Project):
        data = super().to_representation(instance)

        data.update(
            client = ClientProfileSerializer(instance.client).data if instance.client else None,
            team_members = EmployeeProfileSerializer(instance.team_members.all(), many=True).data,
            team_leaders = EmployeeProfileSerializer(instance.team_leaders.all(), many=True).data,
            project_managers = EmployeeProfileSerializer(instance.project_managers.all(), many=True).data,
            tags = ProjectTagsSerializer(instance.tags.all(), many=True).data,
        )
        return data

class ProjectDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDocument
        fields = "__all__"
        extra_kwargs = {
            'project': {'write_only': True},
        }

    def to_representation(self, instance:ProjectDocument):
        data = super().to_representation(instance)

        data.update(
            maker = UserSerializer(instance.maker).data if instance.maker else None,
        )
        return data
    
    
class ProjectTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        fields = "__all__"
        extra_kwargs = {
            'project': {'write_only': True},
            'status':{'read_only': True},
        }

class ProjectTaskResponseSerializer(serializers.ModelSerializer):
    members = EmployeeProfileSerializer(many=True, read_only=True)
    tags = ProjectTagsSerializer(many=True, read_only=True)

    class Meta:
        model = ProjectTask
        fields = "__all__"


class ProjectTaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        exclude = ['project']        