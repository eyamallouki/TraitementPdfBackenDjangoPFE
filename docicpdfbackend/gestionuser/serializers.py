from rest_framework import serializers
from .models import  User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import update_last_login

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=23,min_length=6,write_only=True)
    class Meta:
        model = User
        fields = ('email','username','password','role')

    def validate(self, attrs):
        email = attrs.get('email','')
        username = attrs.get( 'username', '' )

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
            if user:
                if not user.is_active:
                    msg = 'Le compte est désactivé.'
                    raise serializers.ValidationError(msg)
            else:
                msg = 'Impossible de se connecter avec les informations d\'identification fournies.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Veuillez fournir une adresse e-mail et un mot de passe valides.'
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'name']
