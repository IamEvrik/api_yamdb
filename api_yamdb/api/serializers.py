"""Сериализаторы для приложения."""

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import User, Categories, Genres, Titles


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role')


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email')


class UserTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""

    confirmation_code = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)

    class Meta:
        fields = ('username', 'confirmation_code')


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализаторы для категорий."""

    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenresSerializer(serializers.ModelSerializer):
    """Сериализаторы для жанров."""

    class Meta:
        fields = ('name', 'slug')
        model = Genres


class CategoryAtTitleSerializer(serializers.SlugRelatedField):
    def to_representation(self, obj):
        serializer = CategoriesSerializer(obj)
        return serializer.data


class GenreAtTitleSerializer(serializers.SlugRelatedField):
    def to_representation(self, obj):
        serializer = GenresSerializer(obj)
        return serializer.data


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализаторы для произведений."""
    # rating = SlugRelatedField(slug_field='rating', read_only=True)
    genre = GenreAtTitleSerializer(slug_field='slug', many=True,
                                   queryset=Genres.objects.all())
    category = CategoryAtTitleSerializer(slug_field='slug', many=False,
                                         queryset=Categories.objects.all())

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre',
                  'category')
        model = Titles
