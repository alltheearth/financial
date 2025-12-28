"""
Serializers para usuários
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer para perfil de usuário"""

    class Meta:
        model = UserProfile
        fields = [
            'id', 'phone', 'birth_date', 'bio', 'avatar',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Serializer completo de usuário"""

    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_staff', 'is_superuser', 'profile'
        ]
        read_only_fields = ['id', 'is_staff', 'is_superuser']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de usuário"""

    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name'
        ]

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(
                {"password": "As senhas não coincidem."}
            )
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    """Serializer para login"""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError(
                "Username e password são obrigatórios."
            )

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError(
                "Credenciais inválidas."
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "Usuário está inativo."
            )

        data['user'] = user
        return data