from rest_framework import serializers
from .models import User, Role
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import update_last_login

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=23, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'role')

    def validate(self, attrs):
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric characters')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                msg = 'Impossible de se connecter avec les informations d\'identification fournies.'
                raise serializers.ValidationError(msg)
            elif not user.is_active:
                msg = 'Le compte est désactivé.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Veuillez fournir une adresse e-mail et un mot de passe valides.'
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class UserChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    new_password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        new_password2 = attrs.get('new_password2')

        if new_password != new_password2:
            raise serializers.ValidationError("New Password and Confirm New Password don't match")
        return attrs
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']

class AssignUserSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role=Role.ADMINISTRATEUR))

    class Meta:
        model = User
        fields = ['assigned_to']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_verified', 'is_active', 'created_at', 'updated_at']

class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'is_active', 'password']  # Inclure le mot de passe si nécessaire

    def update(self, instance, validated_data):
        # Mettre à jour les champs
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.is_active = validated_data.get('is_active', instance.is_active)

        # Mettre à jour le mot de passe si fourni
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_active']  # Utilise les champs disponibles dans le modèle User
