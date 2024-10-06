import graphene
from graphene_django import DjangoObjectType
from .models import Manga
import traceback

class MangaType(DjangoObjectType):
    class Meta:
        model = Manga
        interfaces = (graphene.relay.node,)
    



class AddMangaFeature(graphene.Mutation):
    success: bool = graphene.Boolean()
    manga: MangaType = graphene.Field(MangaType)
    
class Query(graphene.ObjectType):
    greeting = graphene.String()

    @staticmethod
    def resolve_greeting(root, info):
        return "Hello World"



    
class Mutation(graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
