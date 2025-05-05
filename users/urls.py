from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users import views


urlpatterns = [
    path("register/", views.RegisterUserView.as_view(), name="register-user"),
    path("token/", views.CustomTokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("me/", views.ManageUserView.as_view(), name="me"),
]
