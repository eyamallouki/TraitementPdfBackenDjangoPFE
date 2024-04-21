from django.shortcuts import render
from rest_framework import  generics,status
from .serializers import RegistrationSerializer, PasswordResetRequestSerializer, UserProfileSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import  RefreshToken
from .models import User
from  .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.response import Response
from .utils import Util
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .renderers import UserRenderer  # Assurez-vous d'avoir défini ce rendu
from .serializers import UserChangePasswordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

User = get_user_model()
class RegisterView(generics.CreateAPIView):

    serializer_class = RegistrationSerializer
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user=User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink=reverse('email-veriify')

        absurl = 'https://' + current_site + relativeLink + '?token=' + str( token )
        email_body = 'Bonjour ' + user.username + ',\n Bienvenue à DOCIC ! Veuillez cliquer sur le lien ci-dessous pour vérifier votre adresse e-mail et activer votre compte : Activer votre compte DOCIC \n ' + absurl + ' Merci d\'avoir choisi DOCIC !'
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'activate account DOCIC '}
        Util.send_email( data )

        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(generics.CreateAPIView):
    def get(self, request ):
        token=request.GET.get('token')
        try:
             payload = jwt.decode(token, settings.SECRET_KEY)
             user = User.objects.get(id=payload['user_id'])
             if not user.is_verified:
              user.is_verified = True
              user.save()
             return Response({'email': 'Succfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as  identifier:
            return Response( {'error': 'activation link Expired'}, status=status.HTTP_400_BAD_REQUEST )

        except jwt.exceptions.DecodeError as identifier:
            return Response( {'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST )

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
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_password_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
                reset_password_url = request.build_absolute_uri(reset_password_link)
                email_body = f"Bonjour {user.username},\n Pour réinitialiser votre mot de passe, veuillez cliquer sur le lien suivant : {reset_password_url}"
                Util.send_email({
                    'email_subject': 'Réinitialisation de mot de passe',
                    'email_body': email_body,
                    'to_email': email,
                })
            return Response({'message': 'Un email de réinitialisation de mot de passe a été envoyé.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

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