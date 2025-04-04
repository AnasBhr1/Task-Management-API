from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class TaskSerializer(serializers.ModelSerializer):
    completed_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority', 
                  'status', 'created_at', 'updated_at', 'completed_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_due_date(self, value):
        # Ensure due_date is in the future for new tasks
        if self.instance is None:  # Only for new tasks
            if value < timezone.now():
                raise serializers.ValidationError("Due date must be in the future")
        return value
    
    def validate_priority(self, value):
        valid_priorities = [choice[0] for choice in Task.PRIORITY_CHOICES]
        if value not in valid_priorities:
            raise serializers.ValidationError(
                f"Priority must be one of: {', '.join(valid_priorities)}"
            )
        return value
    
    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in Task.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Status must be one of: {', '.join(valid_statuses)}"
            )
        return value
    
    def validate(self, data):
        # Check if task is completed and being edited
        if self.instance and self.instance.status == 'completed' and 'status' not in data:
            # If task is completed and status is not being changed to pending,
            # prevent other edits
            raise serializers.ValidationError(
                "Completed tasks cannot be edited unless reverted to pending"
            )
        return data
    
    def create(self, validated_data):
        # Assign the current user to the task
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)