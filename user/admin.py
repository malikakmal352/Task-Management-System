from django.contrib import admin
from user.models import Task, Team


# Register your models here.


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin View for AddBank"""

    list_display = ['title', 'creator', 'assign_to', 'status', 'deadline', 'id']
    readonly_fields = ['created',]
    list_filter = ['status', ]
    search_fields = ['title', 'user__username', 'status', ]
    ordering = ['-created', ]


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin View for Team"""
    filter_horizontal = ("members",)

    list_display = ['team_title', 'creator', 'id']
    readonly_fields = ['created',]
    list_filter = ['created', ]
    search_fields = ['team_title', 'user__username']
    ordering = ['-created', ]
