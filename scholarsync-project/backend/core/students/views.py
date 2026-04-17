from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Student
from .serializers import StudentSerializer

User = get_user_model()


def get_request_user(request):
    user_id = request.query_params.get("user_id") or request.data.get("user_id")
    if not user_id:
        return None, Response(
            {"error": "user_id is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None, Response(
            {"error": "User not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    return user, None


def get_student_for_user(user, student_id):
    return Student.objects.filter(id=student_id, user=user).first()


@api_view(["GET"])
def get_students(request):
    user, error_response = get_request_user(request)
    if error_response:
        return error_response

    search_term = (request.query_params.get("search") or "").strip()
    students = Student.objects.filter(user=user).order_by("-created_at")

    if search_term:
        students = students.filter(
            Q(name__icontains=search_term)
            | Q(email__icontains=search_term)
            | Q(grade__icontains=search_term)
        )

    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def add_student(request):
    user, error_response = get_request_user(request)
    if error_response:
        return error_response

    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def update_student(request, id):
    user, error_response = get_request_user(request)
    if error_response:
        return error_response

    student = get_student_for_user(user, id)
    if student is None:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = StudentSerializer(student, data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_student(request, id):
    user, error_response = get_request_user(request)
    if error_response:
        return error_response

    student = get_student_for_user(user, id)
    if student is None:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    student.delete()
    return Response({"message": "Student deleted successfully"})
