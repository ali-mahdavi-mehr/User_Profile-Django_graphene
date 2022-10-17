import graphene
import blog.schema

class Query(blog.schema.Query, graphene.ObjectType):
    pass



schema = graphene.Schema(query=Query)