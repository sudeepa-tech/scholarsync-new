from rest_framework import serializers

from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    enrolled_at = serializers.DateTimeField(source="created_at", read_only=True)

    def validate_email(self, value):
        
        return value.lower()
    
    def validate_phone(self, value):   # ✅ ADD THIS
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        
        if len(value) != 10:
            raise serializers.ValidationError("Phone number must be exactly 10 digits.")
        
        return value
    
    

    class Meta:
        model = Student
        fields = ["id", "user", "name", "email", "phone", "grade", "created_at", "enrolled_at"]
        read_only_fields = ["id", "user", "created_at", "enrolled_at"]
