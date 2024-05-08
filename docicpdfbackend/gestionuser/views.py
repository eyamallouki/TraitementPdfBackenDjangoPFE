from django.contrib.auth import get_user_model
from django.http import JsonResponse

User = get_user_model()
from django.contrib.sites.shortcuts import get_current_site
import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .serializers import (
    RegistrationSerializer,
    PasswordResetRequestSerializer,
    UserProfileSerializer,
    UserLoginSerializer,
    UserChangePasswordSerializer
)

from .utils import Util
from .renderers import UserRenderer
from rest_framework.views import APIView
from rest_framework.response import Response

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('email-veriify')

        absurl = 'http://localhost:4200/auth/email-verify/?token=' + str(token)
        email_body = 'Bonjour ' + user.username + ',\n Bienvenue à DOCIC ! Veuillez cliquer sur le lien ci-dessous pour vérifier votre adresse e-mail et activer votre compte : Activer votre compte DOCIC \n ' + absurl + ' Merci d\'avoir choisi DOCIC !'
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'activate account DOCIC '}
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(generics.CreateAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Succfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'activation link Expired'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': user.role
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                uidb64 = urlsafe_base64_encode(str(user.pk).encode())
                token = PasswordResetTokenGenerator().make_token(user)

                confirmation_url = f"http://localhost:4200/confirmepwd/{uidb64}/{token}"
                reset_password_url = request.build_absolute_uri(confirmation_url)

                email_body = f"Bonjour {user.username},\n Pour réinitialiser votre mot de passe, veuillez cliquer sur le lien suivant : {reset_password_url}\n\nSi vous rencontrez des problèmes avec le lien, vous pouvez également accéder à cette page pour réinitialiser votre mot de passe : {confirmation_url}"
                send_mail('Réinitialisation de mot de passe', email_body, settings.EMAIL_HOST_USER, [email])

                return JsonResponse({'message': 'Un email de réinitialisation de mot de passe a été envoyé.'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'message': 'Aucun utilisateur avec cet email trouvé.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfirmResetPasswordView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserChangePasswordSerializer

    def post(self, request, uidb64, token):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user is not None and PasswordResetTokenGenerator().check_token(user, token):
                new_password = serializer.validated_data['new_password']
                user.set_password(new_password)
                user.save()
                return JsonResponse({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        refresh_token = request.COOKIES.get('refresh_token')  # Récupérer le jeton de rafraîchissement depuis les cookies
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Ajouter le jeton de rafraîchissement à la liste noire
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
