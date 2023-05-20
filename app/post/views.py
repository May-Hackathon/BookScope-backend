from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import (
    Post,
    PostTag,
    PostComment,
)

class PostView(APIView):
    
    authentication_classes = ['TokenAuthentication']
    
    def get(self, request):
        book_name = request.query_params.get('book_name')
        writer_name = request.query_params.get('writer_name')
        search = request.query_params.get('search')
        tags = request.query_params.get('tags')
        
        # TODO:　一つだけかをシリアライザでバリデーションする
        if book_name:
            posts = Post.objects.search_posts_by_book_name(book_name)
        if writer_name:
            posts = Post.objects.search_posts_by_writer_name(writer_name)
        if search:
            posts = Post.objects.search_posts_by_content(search)
        if tags:
            posts = Post.objects.search_posts_by_tags(tags)
        
        return Response(posts)
    
    def post(self, request):
        book_id = request.data.get('read_book_id')
        title = request.data.get('title')
        content = request.data.get('content')
        tags = request.data.get('tags')
        
        post = Post.objects.create_post_with_tags(
            user=request.user,
            read_book_id=book_id,
            title=title,
            content=content,
            tags=tags,
        )
        
        return Response(post)
    
    def put(self, request):
        post_id = request.data.get('post_id')
        title = request.data.get('title')
        content = request.data.get('content')
        tags = request.data.get('tags')
        
        post = Post.objects.get(id=post_id)
        new_post = Post.objects.update_post_with_tags(
            post=post,
            title=title,
            content=content,
            tags=tags,
        )
        
        return new_post
    
    
    def delete(self, request):
        post_id = request.data.get('post_id')
        
        post = Post.objects.get(id=post_id)
        post.delete()
        
        res_json = {
            "message": "success to delete post"
        }
        
        return Response(res_json)