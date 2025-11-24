from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_time', 'end_time', 'is_recurring', 'recurrence_type']
    list_filter = ['is_recurring', 'recurrence_type', 'start_time']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'start_time'

