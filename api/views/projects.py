from rest_framework import viewsets

from api.serializers.projects import ProjectDocumentSerializer, ProjectSerializer, ProjectTagsSerializer, ProjectTaskResponseSerializer, ProjectTaskSerializer, ProjectTaskUpdateSerializer
from projects.models import Project, ProjectDocument, ProjectTags, ProjectTask
from rest_framework.permissions import IsAdminUser

from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

@extend_schema(tags=["Projects"], summary="CRUD operations for Project Tags")
class ProjectTagsViewSet(viewsets.ModelViewSet):
    queryset = ProjectTags.objects.all()
    serializer_class = ProjectTagsSerializer
    permission_classes = [IsAdminUser]

@extend_schema(tags=["Projects"], summary="CRUD operations for Projects")
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminUser]

@extend_schema(tags=["Projects"], summary="CRUD operations for Project Documents")
class ProjectDocumentViewSet(viewsets.ModelViewSet):
    queryset = ProjectDocument.objects.all()
    serializer_class = ProjectDocumentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['project', 'maker']
    permission_classes = [IsAdminUser]


@extend_schema(tags=["Projects"], summary="CRUD operations for Project Documents")
class ProjectTaskViewSet(viewsets.ModelViewSet):
    queryset = ProjectTask.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['project']
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProjectTaskResponseSerializer
        elif self.action in ['create']:
            return ProjectTaskSerializer
        elif self.action in ['update', 'partial_update']:
            return ProjectTaskUpdateSerializer
        # Fallback to default serializer
        return ProjectTaskSerializer
