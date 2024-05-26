from django.urls import path

from userauths import views as userauths_views
from store import views as store_views

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("user/token/", userauths_views.MyTokenObtainPairView.as_view(), name="MyTokenObtainPairView"),
    path("user/token/refresh/   ", TokenRefreshView.as_view(), name="TokenRefreshView"),
    path("user/register/", userauths_views.RegisterView.as_view(), name="RegisterView"),
    path("user/password-reset/<email>/", userauths_views.PasswordResetEmailVerify.as_view(), name="PasswordResetEmailVerify"),
    path("user/password-change/", userauths_views.PasswordChangeView.as_view(), name="PasswordChangeView"),

    path("category/", store_views.CategoryListAPIView.as_view(), name="CategoryListAPIView"),
    path("product/", store_views.ProductListAPIView.as_view(), name="ProductListAPIView"),
    path("product/<slug>/", store_views.ProductDetailAPIView.as_view(), name="ProductDetailAPIView"),
    (path("cart-view/", store_views.CartAPIView.as_view(), name="CartAPIView"))
]
