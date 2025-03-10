
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import UserRegistrationView, UserProfileUpdateView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('profileupdate/',  UserProfileUpdateView.as_view(), name='user-profile-update'),
]
