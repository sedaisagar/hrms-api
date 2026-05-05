from django.urls import path

from api.views.basic import CustomTokenObtainPairView, CustomTokenRefreshView, EmployeeRegistrationView, GetMyProfileView, UserRegistrationView
from api.views.projects import ProjectDocumentViewSet, ProjectTagsViewSet, ProjectViewSet


urlpatterns = [
    path("register/", UserRegistrationView.as_view(),),
    path("employee-register/", EmployeeRegistrationView.as_view(),),
    path("my-profile/", GetMyProfileView.as_view(),),
]

# Auth APIs
urlpatterns += [
    path('login/', CustomTokenObtainPairView.as_view(),),
    path('refresh/', CustomTokenRefreshView.as_view(),),
]


from rest_framework.routers import DefaultRouter

router = DefaultRouter()
from api.views.user import UserViewSetForAdmin,ClientProfileViewsetForAdmin, EmployeeProfileViewsetForAdmin
from api.views.departments import DepartmentViewSet, DesignationViewSet, TeamsViewSet

router.register('users', UserViewSetForAdmin, basename='users')
router.register('client-profile', ClientProfileViewsetForAdmin, basename='client-profile')
router.register('employee-profile', EmployeeProfileViewsetForAdmin, basename='employee-profile')
router.register('departments', DepartmentViewSet, basename='departments')
router.register('designations', DesignationViewSet, basename='designations')
router.register('teams', TeamsViewSet, basename='teams')
router.register('project-tags', ProjectTagsViewSet, basename='project-tags')
router.register('projects', ProjectViewSet, basename='projects')
router.register('project-documents', ProjectDocumentViewSet, basename='project-documents')

urlpatterns += router.urls