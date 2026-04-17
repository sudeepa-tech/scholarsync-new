from rest_framework import serializers

from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    enrolled_at = serializers.DateTimeField(source="created_at", read_only=True)

    class Meta:
        model = Student
        fields = ["id", "user", "name", "email", "phone", "grade", "created_at", "enrolled_at"]
        read_only_fields = ["id", "user", "created_at", "enrolled_at"]
