from django.urls import path

from api.views.basic import CustomTokenObtainPairView, CustomTokenRefreshView, EmployeeRegistrationView, GetMyProfileView, UserRegistrationView


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
from api.views.user import UserViewSetForAdmin,ClientProfileViewsetForAdmin

router.register('users', UserViewSetForAdmin, basename='users')
router.register('client-profile', ClientProfileViewsetForAdmin, basename='client-profile')

urlpatterns += router.urls