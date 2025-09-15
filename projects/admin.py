from django.contrib import admin
from .models import MiniProject

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'status', 'priority', 'due_date', 'created_at')
    list_filter = ('status', 'priority', 'due_date')
    search_fields = ('title', 'description', 'assigned_to__username')

admin.site.register(MiniProject, ProjectAdmin)