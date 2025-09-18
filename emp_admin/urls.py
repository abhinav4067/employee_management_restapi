from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r"fields", views.DynamicFieldViewSet, basename="dynamicfield")

urlpatterns = [
    path("register/", views.RegisterAdminAPIView.as_view(), name="register_admin"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),   # returns access & refresh
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", views.LogoutAPIView.as_view(), name="logout_admin"),
    path("update_admin/", views.UpdateAdminAPIView.as_view(), name="update_admin"),
    path("", include(router.urls)),
]
