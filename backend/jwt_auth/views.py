from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from . import models, serializers


class RegisterUserAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request: Request):
        data = request.data
        user = models.User.objects.create_user(data['username'], data['email'], data['password'])
        return Response(serializers.UserSerializer(user).data, 200)


class RegisterAdminAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request: Request):
        data = request.data
        user = models.User.objects.create_superuser(data['username'], data['email'], data['password'])
        return Response(serializers.UserSerializer(user).data, 200)


class UserInfoAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request):
        return Response(serializers.UserSerializer(request.user).data)


class UserListAPIView(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request: Request):
        return serializers.UserSerializer(models.User.objects.all(), many=True).data
