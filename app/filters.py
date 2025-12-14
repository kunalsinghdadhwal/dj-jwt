"""
Task Tracker Filters

This module defines filter classes for Task model using django-filter.
"""

import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):
    """
    Filter class for Task model.

    Provides filtering capabilities for:
    - status: Exact match
    - priority: Exact match
    - due_date: Range filtering (before, after, exact)
    - created_at: Range filtering
    - is_overdue: Boolean filter (custom)
    """

    # Status filter with exact match
    status = django_filters.ChoiceFilter(
        choices=Task.Status.choices,
        help_text='Filter by task status (todo, in_progress, done)'
    )

    # Priority filter with exact match
    priority = django_filters.ChoiceFilter(
        choices=Task.Priority.choices,
        help_text='Filter by task priority (low, medium, high)'
    )

    # Due date filters
    due_date = django_filters.DateFilter(
        field_name='due_date',
        help_text='Filter by exact due date (YYYY-MM-DD)'
    )
    due_date_before = django_filters.DateFilter(
        field_name='due_date',
        lookup_expr='lte',
        help_text='Filter tasks due on or before this date'
    )
    due_date_after = django_filters.DateFilter(
        field_name='due_date',
        lookup_expr='gte',
        help_text='Filter tasks due on or after this date'
    )

    # Created at filters
    created_after = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte',
        help_text='Filter tasks created after this datetime'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte',
        help_text='Filter tasks created before this datetime'
    )

    # Boolean filter for overdue tasks (custom method filter)
    is_overdue = django_filters.BooleanFilter(
        method='filter_is_overdue',
        help_text='Filter overdue tasks (true/false)'
    )

    class Meta:
        model = Task
        fields = [
            'status',
            'priority',
            'due_date',
            'due_date_before',
            'due_date_after',
            'created_after',
            'created_before',
            'is_overdue',
        ]

    def filter_is_overdue(self, queryset, name, value):
        """
        Filter tasks by overdue status.

        Args:
            queryset: The queryset to filter
            name: The filter name
            value: Boolean value (True for overdue tasks)

        Returns:
            Filtered queryset
        """
        from django.utils import timezone

        if value is True:
            # Overdue: due_date is in the past and status is not done
            return queryset.filter(
                due_date__lt=timezone.now().date()
            ).exclude(status=Task.Status.DONE)
        elif value is False:
            # Not overdue: either no due date, done, or due date in future
            return queryset.exclude(
                due_date__lt=timezone.now().date(),
            ) | queryset.filter(status=Task.Status.DONE)

        return queryset
