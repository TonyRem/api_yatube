from rest_framework import serializers
from django.shortcuts import get_object_or_404

from posts.models import Post, Comment, Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "title", "slug", "description")


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ("id", "text", "author", "image", "group", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    post = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "author", "post", "text", "created")

    def get_post(self, obj):
        return obj.post.pk
