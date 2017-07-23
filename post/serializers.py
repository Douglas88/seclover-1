from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'posts')
        write_only_fields = ('password',)


class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    content = serializers.CharField(required=False, allow_blank=True, max_length=1000)
    user = serializers.ReadOnlyField(source='user.username')

    def create(self, validated_data):
        """
        创建新的Post
        """
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        更新
        """
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

