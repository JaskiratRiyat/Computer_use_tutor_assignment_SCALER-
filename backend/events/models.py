from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Event(models.Model):
    """
    Event model representing calendar events.
    Supports recurring events and handles timezone-aware datetime.
    """
    RECURRENCE_CHOICES = [
        ('none', 'None'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True, null=True)
    color = models.CharField(max_length=7, default='#4285f4')  # Hex color code
    
    # Recurring event fields
    is_recurring = models.BooleanField(default=False)
    recurrence_type = models.CharField(
        max_length=10, 
        choices=RECURRENCE_CHOICES, 
        default='none'
    )
    recurrence_end_date = models.DateTimeField(null=True, blank=True)
    recurrence_interval = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(365)]
    )  # Every N days/weeks/months
    
    # Parent event for recurring series
    parent_event = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='recurring_instances'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['start_time']
        indexes = [
            models.Index(fields=['start_time', 'end_time']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.start_time}"
    
    def check_overlap(self, other_event):
        """
        Check if this event overlaps with another event.
        Returns True if there's an overlap.
        """
        return not (self.end_time <= other_event.start_time or 
                   self.start_time >= other_event.end_time)
    
    def get_duration_minutes(self):
        """Get event duration in minutes."""
        delta = self.end_time - self.start_time
        return int(delta.total_seconds() / 60)

