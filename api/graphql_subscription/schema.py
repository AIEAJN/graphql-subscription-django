import graphene
import traceback

class Query(graphene.ObjectType):
    greeting = graphene.String()

    @staticmethod
    def resolve_greeting(root, info):
        return "Hello World"


schema = graphene.Schema(query=Query)
