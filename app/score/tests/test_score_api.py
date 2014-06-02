from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


GET_SCORE_URL = reverse('score:get_score')


class ScoreApiTests(TestCase):
    """Test the score API"""

    def setUp(self):
        self.client = APIClient()

    def test_get_score_success(self):
        """Test getting score with valid payload is successful"""
        payload = {'phone_number': '4086432477', 'name': 'Test name'}
        res = self.client.post(GET_SCORE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(
            get_user_model()
            .objects.filter(phone_number=payload['phone_number'])
            .exists()
        )
        self.assertTrue('score_overall' in res.data)
