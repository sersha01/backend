from django.urls import path
from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    # TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('', views.userHome, name='home'),
    path('signup/', views.userSignup, name='signup'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('adduser/', views.addUser, name='add_user'),
    path('getusers/', views.getUser, name='get_users'),
    path('updateuser/', views.updateUser, name='update_user'),
    path('userdetails/', views.getUserDetails, name='user_details'),
    path('deleteuser/', views.deleteUser, name='delete_user'),
    path('isadmin/', views.isAdmin, name='is_admin'),
]