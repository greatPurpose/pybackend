from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Coverage

from product.serializers import CoverageSerializer


COVERAGES_URL = reverse('product:coverage-list')


class PublicCoveragesApiTests(TestCase):
    """Test the publicly available Coverages API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving Coverages"""
        res = self.client.get(COVERAGES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCoveragesApiTests(TestCase):
    """Test the authorized user coverages API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            '4086432477',
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_coverages(self):
        """Test retrieving coverages"""
        Coverage.objects.create(user=self.user, name='insurance')
        Coverage.objects.create(user=self.user, name='warranty')

        res = self.client.get(COVERAGES_URL)

        coverages = Coverage.objects.all().order_by('-name')
        serializer = CoverageSerializer(coverages, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_coverages_limited_to_user(self):
        """Test that coverages returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            '4086432478',
            'testpass'
        )
        Coverage.objects.create(user=user2, name='insurance')
        coverage = Coverage.objects.create(user=self.user, name='warranty')

        res = self.client.get(COVERAGES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], coverage.name)

    def test_create_coverage_successful(self):
        """Test creating a new coverage"""
        payload = {'name': 'Test coverage'}
        self.client.post(COVERAGES_URL, payload)

        exists = Coverage.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_coverage_invalid(self):
        """Test creating a new coverage with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(COVERAGES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
