from django.urls import path
from luna_ws import GraphQLSubscriptionHandler


class WSHandler(GraphQLSubscriptionHandler):
    pass

urlpatterns = [
  path('graphql', WSHandler),
]