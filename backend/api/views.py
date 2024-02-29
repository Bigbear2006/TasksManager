from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission
from rest_framework import decorators
from rest_framework.response import Response
from . import models, serializers


class CanManageTask(BasePermission):
    def has_permission(self, request, view):
        if view.action in ('list', 'create'):
            return request.user.is_staff
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user or obj.project.main_user == request.user


class CanManageProject(BasePermission):
    def has_permission(self, request, view):
        if view.action in ('list', 'create'):
            return request.user.is_staff
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.main_user == request.user


class ProjectViewSet(ModelViewSet):
    permission_classes = (CanManageProject,)
    serializer_class = serializers.ProjectSerializer
    queryset = models.Project.objects.all()

    @decorators.action(['GET'], False, 'my')
    def get_user_tasks(self, request):
        projects = models.Project.objects.filter(main_user=request.user)
        return Response(serializers.ProjectSerializer(projects, many=True).data, 200)


class TaskViewSet(ModelViewSet):
    permission_classes = (CanManageTask,)
    serializer_class = serializers.TaskSerializer
    queryset = models.Task.objects.all()

    @decorators.action(['GET'], False, 'my')
    def get_user_tasks(self, request):
        tasks = models.Task.objects.filter(user=request.user)
        return Response(serializers.TaskSerializer(tasks, many=True).data, 200)
