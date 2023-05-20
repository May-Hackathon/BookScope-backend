from django.db import models as DjangoModels
from django.conf import settings

from core import models as CoreModels


class PostModelManager(DjangoModels.Manager):
    def __init__(self) -> None:
        super().__init__()

    def create_post_with_tags(self, user, read_book, title, content, tags):
        post = self.model(user=user, read_book=read_book, title=title, content=content)
        post.save()
        for tag in tags:
            post.tags.add(tag)

        return post

    def update_post_with_tags(self, post, title, content, tags):
        CoreModels.Post.objects.filter(id=post.id).update(title=title, content=content)
        post.tags.clear()
        for tag in tags:
            post.tags.add(tag)

    # ===================　検索系 ===================

    def search_posts_by_book_name(self, title):
        return self.filter(title__contains=title).all()

    def search_posts_by_writer_name(self, writer_name):
        return self.filter(user__name__contains=writer_name).all()

    def search_posts_by_content(self, content):
        return self.filter(content__contains=content).all()

    def search_posts_by_tag(self, tag):
        return self.filter(tags__name__contains=tag).all()

    def search_posts_by_tags(self, tags):
        result = []
        for tag in tags:
            result.extend(self.search_posts_by_tag(tag))
        return result


class Post(DjangoModels.Model):
    class Meta:
        db_table = "posts"
        app_label = "core"

    comments = DjangoModels.ManyToManyField(
        CoreModels.PostComment,
        related_name="posts"
    )
    likes = DjangoModels.ManyToManyField(CoreModels.PostLike, related_name="posts")
    tags = DjangoModels.ManyToManyField(CoreModels.PostTag, related_name="posts")
    
    # 外部キー
    read_book = DjangoModels.ForeignKey(
        CoreModels.ReadBook, on_delete=DjangoModels.CASCADE, related_name="posts"
    )
    user = DjangoModels.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=DjangoModels.CASCADE, related_name="posts"
    )

    # 普通のフィールド
    title = DjangoModels.CharField(max_length=200)
    content = DjangoModels.TextField()
    created_at = DjangoModels.DateTimeField(auto_now_add=True)
    updated_at = DjangoModels.DateTimeField(auto_now=True)

    objects = PostModelManager()

    def str(self):
        return f"title: {self.title} "
