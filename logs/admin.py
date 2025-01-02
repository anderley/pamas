from django.contrib import admin
from .models import LogEntry

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('app', 'level', 'created_at', 'message')
    list_filter = ('level',)
    search_fields = ('message',)
    ordering = ('-created_at',)