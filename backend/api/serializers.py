from rest_framework.serializers import ModelSerializer
from . import models


class TaskSerializer(ModelSerializer):
    class Meta:
        model = models.Task
        fields = '__all__'


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = models.Project
        fields = '__all__'
