from django.test import TestCase
from graphene_django.utils.testing import GraphQLTestCase
from django.urls import reverse
from .models import Manga


class URLTests(TestCase):
    def test_graphql_url(self):
        response = self.client.get(reverse('graphql'))
        self.assertEqual(response.status_code, 400)
        

class QueryTests(GraphQLTestCase):
    def test_greeting(self):
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
        
        
class MutationsTests(GraphQLTestCase):
    def test_add_manga(self):
        response = self.query(
            '''
            mutation addManga(name="Naruto", synopsis="synopsis", author="Masashi Kishimoto"){
                success
                message
                manga{
                    name
                    author
                }
            }
            '''
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertResponseNoErrors(response)
        content = response.json()
        self.assertTrue(content['data']['success'])
        self.assertIsNone(content['data']['message'])
        self.assertEqual(content['data']['manga']["name"], "Naruto")
        self.assertEqual(content['data']['manga']["author"], "Masashi Kishimoto")
        
    def test_add_existing_manga(self):
        Manga.objects.create(name="Naruto", synopsis="synopsis", author="Masashi Kishimoto")
        
        response = self.query(
            '''
            mutation addManga(name="Naruto", synopsis="synopsis", author="Masashi Kishimoto"){
                success
                message
                manga{
                    name
                    author
                }
            }
            '''
        )
        self.assertEqual(response.status_code, 200)
        self.assertResponseHasErrors(response)
        content = response.json()
        self.assertFalse(content['data']['success'])
        self.assertIsNotNone(content['data']['message'])
        self.assertIsNone(content['data']['manga'])
        