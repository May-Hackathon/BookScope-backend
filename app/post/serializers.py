"""
Serializers for Pst API
"""

from rest_framework import serializers

from core.models import (
    Post,
    PostTag,
    PostComment,
    PostLike,
) 

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = ['id', 'name']
        
class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ['id', 'comment']
        
        
class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    comments = PostComment(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'contents', 'tags' ]