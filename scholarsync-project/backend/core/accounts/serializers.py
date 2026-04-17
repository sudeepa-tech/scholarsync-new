import re

from rest_framework import serializers

from .models import User


def build_unique_username(email):
    local_part = email.split("@", 1)[0]
    base_username = re.sub(r"[^a-zA-Z0-9._-]+", "", local_part) or "user"
    username = base_username
    suffix = 1

    while User.objects.filter(username__iexact=username).exists():
        suffix += 1
        username = f"{base_username}{suffix}"

    return username


class RegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=4)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value.lower()

    def create(self, validated_data):
        full_name = validated_data["full_name"].strip()
        first_name, _, last_name = full_name.partition(" ")
        email = validated_data["email"]

        user = User.objects.create_user(
            username=build_unique_username(email),
            email=email,
            password=validated_data["password"],
            first_name=first_name,
            last_name=last_name.strip(),
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "date_joined",
        ]
        read_only_fields = ["id", "date_joined", "full_name"]

    def get_full_name(self, obj):
        return obj.get_full_name().strip() or obj.username
