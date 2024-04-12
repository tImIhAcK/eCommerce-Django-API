from accounts.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django_restql.mixins import DynamicFieldsMixin
from rest_framework import serializers
from .models import User, Profile
from djoser.serializers import UserCreateSerializer
from rest_framework import status
from rest_framework.response import Response
from djoser.serializers import TokenCreateSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)

        token['email'] = user.email
        token['id'] = user.id

        return token


class UserSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id', 'email', 'password']

    def create(self, validated_data):
        user = User(**validated_data)

        email_sent = user.send_activation_email()

        if email_sent:
            return Response(status=status.HTTP_201_CREATED)

        return Response(
            {"message": "Failed to send activation email."},
            status=status.HTTP_400_BAD_REQUEST
        )


class ProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'gender'
            'phone',
            'city',
            'state',
            'country',
            'image'

        ]

    def create(self, validated_data, *args, **kwargs):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data, *args, **kwargs)
