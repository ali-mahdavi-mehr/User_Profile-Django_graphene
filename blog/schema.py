from django.db.models import Q
import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from blog.models import Post
from django.contrib.auth import get_user_model
from graphql import GraphQLError
import graphql_jwt

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields= ["id", "username", "email", "first_name", "last_name", "posts"]



class PostType(DjangoObjectType):
    class Meta:
        model= Post


class PostInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    slug = graphene.String(required=True)
    tags = graphene.String(default_value=None)
    content = graphene.String(default_value=None)

class CreatePost(graphene.Mutation):
    class Arguments:
        input = PostInput()
    status = graphene.Boolean()
    message = graphene.List(graphene.String)
    post = graphene.Field(PostType)

    def mutate(cls, info, input):
        status = False
        message = []
        message.append("Data Received")
        try:
            new_post = Post(
                title=input.title,
                slug=input.slug,
                creator=User.objects.last(),
                tags = input.tags,
                content= input.content
            )
            new_post.save()
            status = True
            message.append("Post Created")

        except Exception as e:
            message += [str(error) for error in e.args ]
        

        return CreatePost(status=status, message=message, post=new_post)


class UpdatePost(graphene.Mutation):
    class Arguments:
        slug = graphene.String(required=True)
        input = PostInput()

    post = graphene.Field(PostType, required=False)
    status = graphene.Boolean()
    message = graphene.List(graphene.String)

    def mutate(root, info, slug, input, **kwargs):
        status = False
        message = []
        message.append("Data Received")
        try:
            post_exist = Post.objects.get(slug=slug)
            if not post_exist:
                raise Exception()
        except Exception as e:
            message.append("Post Not Found!")
            status = False
            return UpdatePost(status=status, message=message)
                
        try:
            p = Post.objects.get(slug=slug)
            message.append("Updating post")

            p.title = input.title
            p.tags = input.tags if  input.content != None else p.tags
            p.content = input.content if input.content != None else p.content
            p.save()
            message.append("Post Updated")
            status = True

        except Exception as e:
            message += [str(error) for error in e.args ]
            return UpdatePost(status=status, message=message)

        
        return UpdatePost(status=status, message=message, post=p)


class DeletePost(graphene.Mutation):
    class Arguments:
        slug = graphene.String()

    status = graphene.Boolean()
    message = graphene.List(graphene.String)

    def mutate(parent, info, slug):
        message = ["Start Deleting"]
        status = False
        try:
            post = Post.objects.get(slug=slug)
            post.delete()
            status = True
            message.append("Post Deleted")

        except Post.DoesNotExist as e:
            message.append(str(e))
        except Exception as e:
            message += [error for error in e.args]

        return DeletePost(status=status, message=message)
            
            

class Query(ObjectType):
    posts = graphene.List(PostType)
    post = graphene.Field(PostType, slug=graphene.String())
    filterd_posts = graphene.List(PostType, title=graphene.String(default_value=""))



    users = graphene.List(UserType) 
    user = graphene.Field(UserType, username=graphene.String())



    def resolve_posts(root, info, **kwargs):
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


class Mutate(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
