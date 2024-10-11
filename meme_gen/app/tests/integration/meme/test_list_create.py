from app.tests.utils import create_test_user, create_meme_template, create_memes
from rest_framework.test import APIClient
from app.models import Meme
from rest_framework import status
from django.urls import reverse
from django.test import TestCase

class MemeListCreateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_test_user()
        self.client.force_authenticate(user=self.user)

        self.template = create_meme_template()
        self.meme_list_url = reverse('meme_list_create')

    def test_list_memes(self):
        create_memes(2, self.template, self.user)

        response = self.client.get(self.meme_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        received_memes = response.data['results']
        self.assertEqual(len(received_memes), 2)

        for i, meme in enumerate(received_memes):
            self.assertEqual(meme['template'], self.template.id)
            self.assertEqual(meme['created_by'], self.user.id)
            self.assertEqual(meme['top_text'], f'Test Top {i}')
            self.assertEqual(meme['bottom_text'], f'Test Bottom {i}')

    def test_create_meme(self):
        meme_data = {
            'template_id': self.template.id,
            'top_text': 'New Top',
            'bottom_text': 'New Bottom'
        }

        response = self.client.post(self.meme_list_url, meme_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Meme.objects.count(), 1)
        created_meme = Meme.objects.first()
        self.assertEqual(created_meme.top_text, 'New Top')
        self.assertEqual(created_meme.bottom_text, 'New Bottom')

    def test_create_meme_with_default_texts(self):
        meme_data = {'template_id': self.template.id}

        response = self.client.post(self.meme_list_url, meme_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Meme.objects.count(), 1)
        created_meme = Meme.objects.first()
        self.assertEqual(created_meme.top_text, self.template.default_top_text)
        self.assertEqual(created_meme.bottom_text, self.template.default_bottom_text)

    def test_create_meme_with_invalid_template(self):
        meme_data = {
            'template_id': 9999,
            'top_text': 'New Top',
            'bottom_text': 'New Bottom'
        }

        response = self.client.post(self.meme_list_url, meme_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Meme.objects.count(), 0)
        self.assertEqual(response.json()['message'], 'Validation error')
        self.assertEqual(response.json()['custom_message'], 'template_id: A meme template with the given ID does not exist.')

    def test_create_meme_with_invalid_data(self):
        meme_data = {
            'template_id': 'not_an_integer',
            'top_text': 'New Top',
            'bottom_text': 'New Bottom'
        }

        response = self.client.post(self.meme_list_url, meme_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Meme.objects.count(), 0)
        self.assertEqual(response.json()['message'], 'Validation error')
        self.assertEqual(response.json()['custom_message'], 'template_id: A valid integer is required.')

    def test_create_meme_with_missing_data(self):
        response = self.client.post(self.meme_list_url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Meme.objects.count(), 0)
        self.assertEqual(response.json()['message'], 'Validation error')
        self.assertEqual(response.json()['custom_message'], 'template_id: This field is required.')

    def test_unauthenticated_user_list(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.meme_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_create(self):
        self.client.force_authenticate(user=None)

        meme_data = {
            'template_id': self.template.id,
            'top_text': 'New Top',
            'bottom_text': 'New Bottom'
        }
        response = self.client.post(self.meme_list_url, meme_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Meme.objects.count(), 0)

    def test_list_memes_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.meme_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_meme_unauthenticated(self):
        self.client.force_authenticate(user=None)
        meme_data = {
            'template_id': self.template.id,
            'top_text': 'Unauthenticated Top',
            'bottom_text': 'Unauthenticated Bottom'
        }
        response = self.client.post(self.meme_list_url, meme_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_memes_pagination(self):
        create_memes(15, self.template, self.user)

        response = self.client.get(self.meme_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])

        second_response = self.client.get(response.data['next'])
        combined_results = response.data['results'] + second_response.data['results']
        unique_meme_ids = set(meme['id'] for meme in combined_results)
        self.assertEqual(len(unique_meme_ids), 15)