import graphene
import traceback
from django.dispatch import receiver
from django.db.models.signals import post_save
import asyncio
from graphene_django import DjangoObjectType, DjangoConnectionField
from .models import Manga

class MangaType(DjangoObjectType):
    class Meta:
        model = Manga
        interfaces = (graphene.relay.Node,)


class AddMangaFeature(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    manga = graphene.Field(MangaType)

    class Arguments:
        name = graphene.String(required=True)
        synopsis = graphene.String()
        author = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        kwargs = {key: value.strip().upper() for key, value in kwargs.items()}
        try:
            manga = Manga.objects.create(**kwargs)
            return AddMangaFeature(success=True, manga=manga)
        except Exception as error:
            error = traceback.format_exc()
            return AddMangaFeature(success=False, message=error)


class Query(graphene.ObjectType):
    greeting = graphene.String()

    @staticmethod
    def resolve_greeting(root, info):
        return "Hello World"

    manga = DjangoConnectionField(MangaType)


class Mutation(graphene.ObjectType):
    add_manga = AddMangaFeature.Field()


new_manga_queue = asyncio.Queue()
@receiver(post_save, sender=Manga)
async def new_manga_signal(sender, instance, **kwargs):
    asyncio.run_coroutine_threadsafe(new_manga_queue.put(instance), asyncio.get_event_loop())


class Subscription(graphene.ObjectType):
    new_manga = graphene.Field(MangaType)
    async def subscribe_new_manga(root, info, **kwargs):
        yield None
        while True: 
            yield await new_manga_queue.get()


schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
