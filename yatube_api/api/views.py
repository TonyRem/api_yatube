from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from posts.models import Post, Comment, Group
from .serializers import PostSerializer, CommentSerializer, GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, *args, **kwargs):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied("Изменение чужого контента запрещено!")
        return super().update(*args, **kwargs)

    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied("Удаление чужого контента запрещено!")
        return super().destroy(*args, **kwargs)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    

    def create(self, request, *args, **kwargs):
        post_id = kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['post'] = post
        self.perform_create(serializer)


    def update(self, *args, **kwargs):
        instance = self.get_object()
        if instance.author!= self.request.user:
            raise PermissionDenied("Изменение чужого контента запрещено!")
        return super().update(*args, **kwargs)
    
    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        if instance.author!= self.request.user:
            raise PermissionDenied("Удаление чужого контента запрещено!")
        return super().destroy(*args, **kwargs)



