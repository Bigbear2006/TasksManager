from django.db import models
from jwt_auth.models import User


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    main_user = models.ForeignKey(User, models.SET_NULL, 'projects', null=True)

    def __str__(self):
        return self.title


# class Reward(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#
#     def __str__(self):
#         return self.title


class Task(models.Model):
    LOW_PRIORITY = 'low'
    MEDIUM_PRIORITY = 'medium'
    HIGH_PRIORITY = 'high'

    PRIORITIES = (
        (LOW_PRIORITY, 'низкий'),
        (MEDIUM_PRIORITY, 'средний'),
        (HIGH_PRIORITY, 'высокий')
    )

    STATUS_PLANNED = 'planned'
    STATUS_PROCESS = 'process'
    STATUS_DONE = 'done'

    STATUSES = (
        (STATUS_PLANNED, 'планируется'),
        (STATUS_PROCESS, 'в процессе'),
        (STATUS_DONE, 'выполнено')
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    priority = models.CharField(max_length=7, choices=PRIORITIES)
    status = models.CharField(max_length=11, choices=STATUSES)
    user = models.ForeignKey(User, models.SET_NULL, 'tasks', null=True)
    project = models.ForeignKey(Project, models.CASCADE, 'tasks')

    def __str__(self):
        return self.title
