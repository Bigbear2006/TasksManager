from rest_framework.serializers import ModelSerializer
from . import models


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'
        read_only_fields = ('is_superuser', 'is_staff')
        extra_kwargs = {
            'password': {'write_only': True}
        }
