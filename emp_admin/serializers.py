from django.contrib.auth.models import User
from rest_framework import serializers
from .models import DynamicField, UserProfile


class RegisterAdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data, is_staff=True, is_superuser=True)
        return user


class UpdateAdminSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source="profile.phone", required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password", "phone"]
        extra_kwargs = {"password": {"write_only": True, "required": False}}

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        UserProfile.objects.update_or_create(
            user=instance, defaults={"phone": profile_data.get("phone")}
        )

        return instance


class DynamicFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicField
        fields = "__all__"
