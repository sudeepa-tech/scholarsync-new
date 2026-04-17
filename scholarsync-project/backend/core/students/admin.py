from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'grade', 'user', 'created_at')
    search_fields = ('name', 'email', 'user__username')
    list_filter = ('grade', 'created_at')

# Register your models here.
admin.site.register(Student, StudentAdmin)
