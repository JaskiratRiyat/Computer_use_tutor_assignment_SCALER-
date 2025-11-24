from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from dateutil.rrule import rrule, DAILY, WEEKLY, MONTHLY, YEARLY
from dateutil.parser import parse

from .models import Event
from .serializers import EventSerializer, EventListSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Event CRUD operations.
    Handles event creation, retrieval, updating, and deletion.
    Also handles recurring event expansion and overlap detection.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        return EventSerializer
    
    def get_queryset(self):
        """
        Filter events by date range if provided.
        Supports query parameters: start_date, end_date
        """
        queryset = Event.objects.all()
        
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            try:
                start_date = parse(start_date)
                queryset = queryset.filter(end_time__gte=start_date)
            except (ValueError, TypeError):
                pass
        
        if end_date:
            try:
                end_date = parse(end_date)
                queryset = queryset.filter(start_time__lte=end_date)
            except (ValueError, TypeError):
                pass
        
        return queryset.order_by('start_time')
    
    def perform_create(self, serializer):
        """
        Create event and handle recurring event generation.
        """
        event = serializer.save()
        
        # If recurring, generate recurring instances
        if event.is_recurring and event.recurrence_type != 'none':
            self._generate_recurring_events(event)
    
    def perform_update(self, serializer):
        """
        Update event. If it's part of a recurring series, handle appropriately.
        """
        instance = serializer.save()
        
        # If updating to recurring, generate instances
        if instance.is_recurring and instance.recurrence_type != 'none' and not instance.parent_event:
            # Delete old instances if any
            Event.objects.filter(parent_event=instance).delete()
            self._generate_recurring_events(instance)
    
    def _generate_recurring_events(self, parent_event):
        """
        Generate recurring event instances based on recurrence settings.
        """
        if not parent_event.is_recurring:
            return
        
        # Map recurrence types to rrule frequencies
        freq_map = {
            'daily': DAILY,
            'weekly': WEEKLY,
            'monthly': MONTHLY,
            'yearly': YEARLY,
        }
        
        freq = freq_map.get(parent_event.recurrence_type)
        if not freq:
            return
        
        # Calculate duration
        duration = parent_event.end_time - parent_event.start_time
        
        # Generate recurring dates
        dates = list(rrule(
            freq=freq,
            interval=parent_event.recurrence_interval,
            dtstart=parent_event.start_time,
            until=parent_event.recurrence_end_date
        ))
        
        # Create event instances (skip first one as it's the parent)
        for date in dates[1:]:
            Event.objects.create(
                title=parent_event.title,
                description=parent_event.description,
                start_time=date,
                end_time=date + duration,
                location=parent_event.location,
                color=parent_event.color,
                is_recurring=True,
                recurrence_type=parent_event.recurrence_type,
                recurrence_end_date=parent_event.recurrence_end_date,
                recurrence_interval=parent_event.recurrence_interval,
                parent_event=parent_event
            )
    
    @action(detail=False, methods=['get'])
    def check_overlap(self, request):
        """
        Check if a new event would overlap with existing events.
        Query params: start_time, end_time, exclude_id (optional)
        """
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')
        exclude_id = request.query_params.get('exclude_id')
        
        if not start_time or not end_time:
            return Response(
                {'error': 'start_time and end_time are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            start_time = parse(start_time)
            end_time = parse(end_time)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid date format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if end_time <= start_time:
            return Response(
                {'error': 'end_time must be after start_time'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check for overlaps
        queryset = Event.objects.filter(
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        
        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)
        
        overlapping_events = queryset.values('id', 'title', 'start_time', 'end_time')
        
        return Response({
            'has_overlap': overlapping_events.exists(),
            'overlapping_events': list(overlapping_events)
        })
    
    @action(detail=False, methods=['get'])
    def by_date_range(self, request):
        """
        Get events within a date range with expanded recurring events.
        Query params: start_date, end_date
        """
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not start_date or not end_date:
            return Response(
                {'error': 'start_date and end_date are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            start_date = parse(start_date)
            end_date = parse(end_date)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid date format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get all events that might overlap with the range
        events = Event.objects.filter(
            start_time__lte=end_date,
            end_time__gte=start_date
        )
        
        # Expand recurring events
        expanded_events = []
        for event in events:
            if event.is_recurring and event.parent_event is None:
                # This is a parent recurring event, expand it
                instances = self._expand_recurring_event(event, start_date, end_date)
                expanded_events.extend(instances)
            elif event.parent_event is None:
                # Regular event or recurring instance
                expanded_events.append(event)
        
        serializer = EventListSerializer(expanded_events, many=True)
        return Response(serializer.data)
    
    def _expand_recurring_event(self, parent_event, start_date, end_date):
        """
        Expand a recurring event into individual instances within date range.
        """
        if not parent_event.is_recurring:
            return [parent_event]
        
        freq_map = {
            'daily': DAILY,
            'weekly': WEEKLY,
            'monthly': MONTHLY,
            'yearly': YEARLY,
        }
        
        freq = freq_map.get(parent_event.recurrence_type)
        if not freq:
            return [parent_event]
        
        duration = parent_event.end_time - parent_event.start_time
        effective_end = min(parent_event.recurrence_end_date, end_date) if parent_event.recurrence_end_date else end_date
        
        dates = list(rrule(
            freq=freq,
            interval=parent_event.recurrence_interval,
            dtstart=parent_event.start_time,
            until=effective_end
        ))
        
        instances = []
        for date in dates:
            if start_date <= date <= end_date:
                # Create a virtual instance (not saved to DB)
                instance = Event(
                    id=parent_event.id,  # Use parent ID for identification
                    title=parent_event.title,
                    description=parent_event.description,
                    start_time=date,
                    end_time=date + duration,
                    location=parent_event.location,
                    color=parent_event.color,
                    is_recurring=True,
                    recurrence_type=parent_event.recurrence_type,
                    parent_event=parent_event
                )
                instances.append(instance)
        
        return instances

