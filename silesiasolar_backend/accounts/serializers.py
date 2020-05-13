from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

from influx_updater.utils import create_influx_account
from influx_updater.exceptions import InfluxUserNotCreated

# serialize user data required for registration
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        fields = '__all__'
        model = User


    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']

        # provided username already in database
        if len(User.objects.filter(username=username)) != 0:
            raise serializers.ValidationError({"error": "Provided username is already taken"})

        # provided email already in database
        if len(User.objects.filter(email=email)) != 0:
            raise serializers.ValidationError({"error": "Provided email is already taken"})

        # try to create influx account
        try:
            create_influx_account(username=username, password=password)
        except InfluxUserNotCreated:
            raise serializers.ValidationError({"error": "Some problem occurred, user cannot be registered"})

        user = User.objects.create_user(username, email, password)
        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = '__all__'


    def save(self):
        user = authenticate(**self.validated_data)
        if user:
            return user
        raise serializers.ValidationError({"error": "Incorrect credentials"})