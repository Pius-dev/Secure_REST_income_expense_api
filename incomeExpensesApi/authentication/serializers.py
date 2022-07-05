
from asyncore import read
from dataclasses import field
from pyexpat import model
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    
    class Meta:
        model = User
        fields = ['email', 'username', 'password']


    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                'This username should only contain alphanumeric charaters'
            )
        return attrs

    def create(self, validated_date):
        return User.objects.create_user(**validated_date)

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=599)

    class Meta:
        model = User
        fields = ['token'] 

# set up a serializer login class
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255, min_length=4)
    password=serializers.CharField(max_length=200, min_length=6, write_only=True)
    username=serializers.CharField(max_length=200, min_length=3, read_only=True)
    tokens=serializers.CharField(max_length=200, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']


    # authenticate the user
    def validate(self, attrs):
        email=attrs.get('email', '')
        password=attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')

        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username':user.username,
            'tokens': user.tokens
            
        }
    