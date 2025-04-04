from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'due_date', 'priority', 'status', 'created_at')
    list_filter = ('status', 'priority', 'user')
    search_fields = ('title', 'description')
    date_hierarchy = 'due_date'