from django.urls import path

from userauths import views as userauths_views

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("user/token/", userauths_views.MyTokenObtainPairView.as_view(), name="MyTokenObtainPairView"),
    path("user/token/refresh/   ", TokenRefreshView.as_view(), name="TokenRefreshView"),
    path("user/register/", userauths_views.RegisterView.as_view(), name="RegisterView"),
    path("user/password-reset/<email>/", userauths_views.PasswordResetEmailVerify.as_view(), name="PasswordResetEmailVerify"),
    path("user/password-change/", userauths_views.PasswordChangeView.as_view(), name="PasswordChangeView")
]
