from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Comment, Group, Post, Follow

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователей."""
    posts = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='posts',
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'posts')


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор модели постов."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор модели групп."""
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор модели подписок."""
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow

    def validate(self, data):
        user = self.context['request'].user
        following = data['following']
        is_unique = Follow.objects.filter(
            user=user,
            following=following
        )
        if user == following:
            raise serializers.ValidationError(
                'Вы не можете быть подписаны на самого себя.'
            )
        if len(is_unique) != 0:
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора.'
            )
        return data
