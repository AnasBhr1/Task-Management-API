from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Foreign key to User model
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    
    def __str__(self):
        return self.title
    
    def clean(self):
        # Validate that due_date is in the future for new tasks
        if self.due_date and not self.id:  # Only for new tasks
            if self.due_date < timezone.now():
                raise ValidationError({'due_date': 'Due date must be in the future'})
    
    def save(self, *args, **kwargs):
        # If status is changed to completed, set completed_at timestamp
        if self.pk:
            try:
                old_task = Task.objects.get(pk=self.pk)
                if old_task.status != 'completed' and self.status == 'completed':
                    self.completed_at = timezone.now()
                elif old_task.status == 'completed' and self.status != 'completed':
                    self.completed_at = None
            except Task.DoesNotExist:
                pass
        
        self.clean()
        super().save(*args, **kwargs)