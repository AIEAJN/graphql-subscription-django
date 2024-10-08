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
    class Meta:
        description = """
```
mutation addManga($name: String = "Bleach", $synopsis: String = "Synopsis", $author: String = "Tite Kubo") {
  addManga(name: $name, synopsis: $synopsis, author: $author) {
    success
    message
    manga {
      id
      name
      author
      createdDate
    }
  }
}
```        
"""
    @classmethod
    def mutate(cls, root, info, **kwargs):
        kwargs = {key: value.strip().upper() for key, value in kwargs.items()}
        try:
            manga = Manga.objects.create(**kwargs)
            return AddMangaFeature(success=True, manga=manga)
        except Exception as error:
            error = "This manga and its author already exist together!"
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


new_manga_description = """
```
subscription subscribeToNewManga {
  newManga {
    id
    name
    synopsis
    author
    createdDate
  }
}
```        
"""
class Subscription(graphene.ObjectType):
    new_manga = graphene.Field(MangaType, description=new_manga_description)
    async def subscribe_new_manga(root, info, **kwargs):
        yield None
        while True: 
            yield await new_manga_queue.get()


schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
