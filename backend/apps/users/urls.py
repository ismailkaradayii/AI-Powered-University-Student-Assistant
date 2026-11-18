from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CurrentUserView, StudentLoginView

urlpatterns = [
    path("login/", StudentLoginView.as_view(), name="student-login"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("me/", CurrentUserView.as_view(), name="current-user"),
]
