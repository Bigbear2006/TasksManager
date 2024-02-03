from rest_framework.serializers import ModelSerializer
from . import models


class TaskSerializer(ModelSerializer):
    class Meta:
        model = models.Task
        fields = '__all__'


class ProjectSerializer(ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = models.Project
        fields = ('title', 'description', 'created_at', 'main_user', 'tasks')
