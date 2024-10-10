from django.contrib.auth.models import User
from rest_framework.test import APIClient
from app.models import Meme, MemeTemplate
from rest_framework import status
from django.urls import reverse
from django.test import TestCase

class MemeListCreateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.force_authenticate(user=self.user)

        self.template = MemeTemplate.objects.create(name='Test Template', default_top_text='Top', default_bottom_text='Bottom')
        self.meme_list_url = reverse('meme_list_create')

    def create_meme(self, top_text='Test Top', bottom_text='Test Bottom'):
        return Meme.objects.create(
            template=self.template,
            top_text=top_text,
            bottom_text=bottom_text,
            created_by=self.user
        )

    def test_list_memes(self):
        self.create_meme()
        self.create_meme('Another Top', 'Another Bottom')

        response = self.client.get(self.meme_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        received_memes = response.data['results']
        self.assertEqual(len(received_memes), 2)

        for i, meme in enumerate(received_memes):
            self.assertEqual(meme['template'], self.template.id)
            self.assertEqual(meme['created_by'], self.user.id)
            self.assertEqual(meme['top_text'], 'Test Top' if i == 0 else 'Another Top')
            self.assertEqual(meme['bottom_text'], 'Test Bottom' if i == 0 else 'Another Bottom')

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
        self.assertEqual(created_meme.top_text, 'Top')
        self.assertEqual(created_meme.bottom_text, 'Bottom')

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
        for i in range(15):
            self.create_meme(f'Top {i}', f'Bottom {i}')

        response = self.client.get(self.meme_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])

        second_response = self.client.get(response.data['next'])
        combined_results = response.data['results'] + second_response.data['results']
        unique_meme_ids = set(meme['id'] for meme in combined_results)
        self.assertEqual(len(unique_meme_ids), 15)