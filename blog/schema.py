from django.db.models import Q
from typing import Optional
import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from blog.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields= ["id", "username", "email", "first_name", "last_name", "posts"]



class PostType(DjangoObjectType):
    class Meta:
        model= Post




class Query(ObjectType):
    posts = graphene.List(PostType)
    post = graphene.Field(PostType, slug=graphene.String())
    filterd_posts = graphene.List(PostType, title=graphene.String(default_value=""))


    users = graphene.List(UserType) 
    user = graphene.Field(UserType, username=graphene.String())



    def resolve_posts(root, **kwargs):
        return Post.objects.all()

    def resolve_filterd_posts(root, info, title, **kwargs):
        return Post.objects.filter(Q(title__icontains=title))

    def resolve_post(root, info, slug, **kwargs):
        post = Post.objects.get(slug=slug)
        return post




    def resolve_users(root, **kwargs):
        return User.objects.all()

    def resolve_user(root, info, username, **kwargs):
        user = User.objects.get(username=username)
        return user

