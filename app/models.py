"""
Task Tracker Models

This module defines the Task model for the Task Tracker API.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Task(models.Model):
    """
    Task model representing a user's task.

    Each task belongs to a specific user and includes fields for
    tracking status, priority, and due dates.
    """

    class Status(models.TextChoices):
        """Task status choices."""
        TODO = 'todo', 'To Do'
        IN_PROGRESS = 'in_progress', 'In Progress'
        DONE = 'done', 'Done'

    class Priority(models.TextChoices):
        """Task priority choices."""
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    # Required fields
    title = models.CharField(
        max_length=255,
        help_text='The title of the task'
    )

    # Optional fields
    description = models.TextField(
        blank=True,
        default='',
        help_text='Detailed description of the task'
    )

    # Status and priority with defaults
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
        help_text='Current status of the task'
    )

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        help_text='Priority level of the task'
    )

    # Due date (optional)
    due_date = models.DateField(
        null=True,
        blank=True,
        help_text='Due date for the task'
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='When the task was created'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='When the task was last updated'
    )

    # Owner relationship
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        help_text='The user who owns this task'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', 'priority']),
            models.Index(fields=['user', 'due_date']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'{self.title} ({self.get_status_display()})'

    @property
    def is_overdue(self):
        """Check if the task is overdue."""
        if self.due_date and self.status != self.Status.DONE:
            return self.due_date < timezone.now().date()
        return False
