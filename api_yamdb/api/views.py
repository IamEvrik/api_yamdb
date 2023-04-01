"""View и viewsets для приложения."""

from rest_framework import (filters, generics, mixins, permissions, response,
                            status, views, viewsets)
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.tokens import default_token_generator
from django.core import exceptions
from django.core.mail.message import EmailMessage
from django.shortcuts import get_object_or_404

from api.permissions import UserIsAdmin
from api.serializers import (UserRegistrationSerializer, UserSerializer,
                             UserTokenSerializer)
from reviews.models import User


class UserViewSet(viewsets.ModelViewSet):
    """Работа с пользователями."""

    queryset = User.objects.all()
    permission_classes = (UserIsAdmin,)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(methods=['get', 'patch'], detail=False, permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        user = get_object_or_404(User, username=request.user)
        serializer = self.get_serializer(user)
        if request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data)
            if serializer.is_valid():
                serializer.validated_data['role'] = user.role
                serializer.save(user=user)
                return response.Response(serializer.data)
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response.Response(serializer.data)


class UserRegistrationViewSet(views.APIView):
    """Регистрация пользователя."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """При создании нового пользователя отправляем код подтверждения на почту."""
        try:
            new_user = User.objects.get(
                username=request.data.get('username'),
                email=request.data.get('email')
            )
        except exceptions.ObjectDoesNotExist:
            serializer = UserRegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            new_user = serializer.save()
        confirm_code = default_token_generator.make_token(new_user)
        message = EmailMessage(
            subject='YamDB confirmation code',
            body=f'confirmation code for {new_user.username} is {confirm_code}',
            from_email='yamdb@no    reply.com',
            to=(request.data['email'],),
                
        )
        message.send(fail_silently=True)
        response_text = {
            'username': new_user.username,
            'email': new_user.email
        }
        return response.Response(response_text, status=status.HTTP_200_OK)


class UserGetToken(views.APIView):
    """Выдача токена пользователю."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserTokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            user = get_object_or_404(User, username=username)
            conf_code = serializer.validated_data.get('confirmation_code')
            if default_token_generator.check_token(user, conf_code):
                token = RefreshToken.for_user(user)
                return response.Response({'token': str(token.access_token)})
            return response.Response(
                {'error': 'invalid code'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
