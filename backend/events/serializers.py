from rest_framework import serializers
from .models import Event
from django.utils import timezone
from datetime import datetime, timedelta
from dateutil.rrule import rrule, DAILY, WEEKLY, MONTHLY, YEARLY


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Event model with validation for overlaps and recurring events.
    """
    duration_minutes = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'start_time', 'end_time',
            'location', 'color', 'is_recurring', 'recurrence_type',
            'recurrence_end_date', 'recurrence_interval', 'parent_event',
            'created_at', 'updated_at', 'duration_minutes'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'parent_event']
    
    def validate(self, data):
        """
        Validate event data:
        1. End time must be after start time
        2. Check for overlaps with existing events (optional, can be handled in frontend)
        3. Validate recurring event settings
        """
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        
        if start_time and end_time:
            if end_time <= start_time:
                raise serializers.ValidationError({
                    'end_time': 'End time must be after start time.'
                })
        
        # Validate recurring event settings
        is_recurring = data.get('is_recurring', False)
        recurrence_type = data.get('recurrence_type', 'none')
        recurrence_end_date = data.get('recurrence_end_date')
        
        if is_recurring:
            if recurrence_type == 'none':
                raise serializers.ValidationError({
                    'recurrence_type': 'Recurrence type must be specified for recurring events.'
                })
            if not recurrence_end_date:
                raise serializers.ValidationError({
                    'recurrence_end_date': 'Recurrence end date is required for recurring events.'
                })
            if recurrence_end_date <= start_time:
                raise serializers.ValidationError({
                    'recurrence_end_date': 'Recurrence end date must be after start time.'
                })
        
        return data


class EventListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing events.
    """
    duration_minutes = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'start_time', 'end_time',
            'location', 'color', 'is_recurring', 'recurrence_type',
            'duration_minutes'
        ]

