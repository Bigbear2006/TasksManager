from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from . import models, serializers


class RegisterUserAPIView(APIView):
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
    def post(self, request: Request):
        return Response(serializers.UserSerializer(request.user).data)
