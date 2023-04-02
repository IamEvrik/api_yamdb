"""View и viewsets для приложения."""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, mixins, permissions, response, status,
                            views,
                            viewsets)
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.tokens import default_token_generator
from django.core import exceptions
from django.core.mail.message import EmailMessage
from django.shortcuts import get_object_or_404

from api_yamdb.filters import TitleFilter
from api.permissions import UserIsAdmin, IsAdminOrReadOnly
from api.serializers import (UserRegistrationSerializer, UserSerializer,
                             UserTokenSerializer, CategoriesSerializer,
                             GenresSerializer, TitlesSerializer)
from reviews.models import User, Categories, Genres, Titles


class UserViewSet(viewsets.ModelViewSet):
    """Работа с пользователями."""

    queryset = User.objects.all()
    permission_classes = (UserIsAdmin,)
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'patch', 'delete', 'post')

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        """Ответ на /me/."""
        user = get_object_or_404(User, username=request.user)
        serializer = self.get_serializer(user)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.validated_data['role'] = user.role
                serializer.save(user=user)
                return response.Response(serializer.data)
            return response.Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return response.Response(serializer.data)


class UserRegistrationViewSet(views.APIView):
    """Регистрация пользователя."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """Отправляем код подтверждения на почту."""
        try:
            user = User.objects.get(
                username=request.data.get('username'),
                email=request.data.get('email')
            )
        except exceptions.ObjectDoesNotExist:
            serializer = UserRegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        confirm_code = default_token_generator.make_token(user)
        message = EmailMessage(
            subject='YamDB confirmation code',
            body=f'confirmation code for {user.username} is {confirm_code}',
            from_email='yamdb@no    reply.com',
            to=(request.data['email'],),
        )
        message.send(fail_silently=True)
        response_text = {
            'username': user.username,
            'email': user.email
        }
        return response.Response(response_text, status=status.HTTP_200_OK)


class UserGetToken(views.APIView):
    """Выдача токена пользователю."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """Генерация токена доступа."""
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
        return response.Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CustomizeViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """Кастомизированный вьюсет только на просмотр, создание и удаление"""

    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name',)


class CategoriesViewSet(CustomizeViewSet):
    """Вьюсет для категорий."""

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(CustomizeViewSet):
    """Вьюсет для жанров."""

    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений."""

    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
