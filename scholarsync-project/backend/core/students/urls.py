from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_students, name='get_students'),
    path('add/', views.add_student, name='add_student'),
    path('update/<int:id>/', views.update_student, name='update_student'),
    path('delete/<int:id>/', views.delete_student, name='delete_student'),
]