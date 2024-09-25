from django.test import TestCase
from graphene_django.utils.testing import GraphQLTestCase
from django.urls import reverse
from .models import AppConfig

class URLTests(TestCase):
    def test_graphql_url(self):
        # Data initialization
        AppConfig.objects.create(allow_introspection=True)
        self.assertTrue(AppConfig.objects.filter(allow_introspection=True).exists())
        response = self.client.get(reverse('graphql'))
        self.assertEqual(response.status_code, 400)
        

class QueryTests(GraphQLTestCase):
    def test_greeting(self):
        # Data initialization
        AppConfig.objects.create(allow_introspection=True)
        self.assertTrue(AppConfig.objects.filter(allow_introspection=True).exists())
        response = self.query(
            '''
            query{
                greeting
            }
            ''',
        )
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['greeting'], 'Hello World')