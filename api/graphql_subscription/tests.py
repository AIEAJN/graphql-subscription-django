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
        
    def test_manga(self):
        Manga.objects.create(name="NARUTO", synopsis="synopsis", author="MASASHI KISHIMOTO")
        response = self.query(
            '''
            query{
                manga{
                    edges{
                        node{
                            name
                            author
                        }
                    }
                }
            }
            ''',
        )
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertEqual(content['data']['manga']['edges'][0]['node']['name'], 'NARUTO')
        self.assertEqual(content['data']['manga']['edges'][0]['node']['author'], 'MASASHI KISHIMOTO')

        
        
class MutationsTests(GraphQLTestCase):
    def test_add_manga(self):
        response = self.query(
            '''
            mutation{
                addManga(name: "Naruto", synopsis: "synopsis" author: "Masashi Kishimoto"){
                    success
                    message
                    manga{
                        name
                        author
                    }
                }
            }
            '''
        )
        
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertTrue(content['data']['addManga']['success'])
        self.assertIsNone(content['data']['addManga']['message'])
        self.assertEqual(content['data']['addManga']['manga']["name"], "NARUTO")
        self.assertEqual(content['data']['addManga']['manga']["author"], "MASASHI KISHIMOTO")
        
    def test_add_existing_manga(self):
        Manga.objects.create(name="NARUTO", synopsis="synopsis", author="MASASHI KISHIMOTO")
        response = self.query(
            '''
            mutation{
                addManga(name: "Naruto", synopsis: "synopsis" author: "Masashi Kishimoto"){
                    success
                    message
                    manga{
                        name
                        author
                    }
                }
            }
            '''
        )
        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertFalse(content['data']['addManga']['success'])
        self.assertIsNotNone(content['data']['addManga']['message'])
        self.assertIsNone(content['data']['addManga']['manga'])
        