from django.contrib.auth.models import User
from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

from .models import DynamicField, UserProfile
from .serializers import (
    RegisterAdminSerializer,
    UpdateAdminSerializer,
    DynamicFieldSerializer,
)


# ---------------------------
# Admin Registration
# ---------------------------
class RegisterAdminAPIView(generics.CreateAPIView):
    serializer_class = RegisterAdminSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save(is_staff=True, is_superuser=True)
        return Response(
            {"status": "success", "message": "Admin registered successfully"},
            status=status.HTTP_201_CREATED,
        )


# ---------------------------
# Update Admin Profile
# ---------------------------
class UpdateAdminAPIView(generics.UpdateAPIView):
    serializer_class = UpdateAdminSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


# ---------------------------
# Logout (Blacklist refresh token)
# ---------------------------
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "detail": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


# ---------------------------
# Admin Dashboard (dummy API)
# ---------------------------
class AdminDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Welcome to the admin dashboard!"})


# ---------------------------
# Form Designer View
# ---------------------------
class FormDesignerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        fields = DynamicField.objects.values("id", "label", "field_type")
        return Response({"fields": fields})


# ---------------------------
# Dynamic Field CRUD
# ---------------------------
class DynamicFieldViewSet(viewsets.ModelViewSet):
    queryset = DynamicField.objects.all()
    serializer_class = DynamicFieldSerializer
    permission_classes = [IsAuthenticated]
