from django.db import IntegrityError
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Parameter, FORMAT_EMAIL, TYPE_STRING, TYPE_INTEGER, IN_FORM, IN_QUERY

from .models import User
from .serializers import UserSerializer
from .utils import send_email


class RegisterUserAPIView(GenericAPIView):
    serializer_class = UserSerializer

    @swagger_auto_schema(responses={200: UserSerializer(), 400: 'user with that email already exists'})
    def post(self, request: Request):
        data = request.data
        try:
            user = User.objects.create_user(data['username'], data['email'], data['password'], is_active=False)
        except IntegrityError:
            user = User.objects.get(email=data['email'])
            if user.is_active:
                return Response({'error': 'user with that email already exists'}, 400)
            user.username = data['username']
            user.set_password(data['password'])

        send_email(user)
        return Response(self.serializer_class(user).data, 200)


class UserInfoAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @swagger_auto_schema(responses={200: UserSerializer()})
    def get(self, request: Request):
        return Response(self.serializer_class(request.user).data)


class UsersListAPIView(GenericAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = UserSerializer

    def get(self, request: Request):
        return Response(self.serializer_class(User.objects.all(), many=True).data, 200)


class VerifyEmailAPIView(APIView):
    @swagger_auto_schema(manual_parameters=[
        Parameter('user_id', IN_QUERY, type=TYPE_INTEGER),
        Parameter('token', IN_QUERY, type=TYPE_STRING)
    ])
    def get(self, request: Request):
        user_id = request.query_params.get('user_id', None)
        token = request.query_params.get('token', None)
        try:
            user = User.objects.get(id=user_id)
        except:
            user = None

        if user is None:
            return Response({'error': 'user does not exists'}, 400)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'invalid token'}, 400)

        user.is_active = True
        user.save()

        return Response(status=204)


class SendEmailAgain(APIView):
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(manual_parameters=[
        Parameter('email', IN_FORM, type=TYPE_STRING, format=FORMAT_EMAIL)
    ])
    def post(self, request: Request):
        user = User.objects.get(email=request.data['email'])
        if not user.is_active:
            send_email(user)
            return Response(status=204)
        return Response({'error': 'user already is active'}, 400)
