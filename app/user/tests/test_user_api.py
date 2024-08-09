"""Test user API"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from community.models import Community
from datetime import date

import logging


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """Create new user."""
    return get_user_model().objects.create_user(**params)


class A_PublicUserApiTests(TestCase):
    """Test public API"""

    @classmethod
    def setUpTestData(cls):
        """Setup data for the whole TestCase."""
        cls.community = Community.objects.create(
            name='Test Community',
            expiration_date=date(2025, 12, 31),
            status=True,
        )
        cls.admin_payload = {
            'email': 'user@example.com',
            'password': 'testpass123',
            'name': 'Admin Name',
            'is_admin': True,
            # 'community_id': cls.community,
        }
        cls.admin_user = create_user(**cls.admin_payload)

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
        self.logger = logging.getLogger('django.request')
        self.original_logging_level = self.logger.level
        self.logger.setLevel(logging.ERROR)

    def test_a01_create_user_successful(self):
        """Test create new user successful."""

        coach_payload = {
            'email': 'coach@example.com',
            'password': 'coach_pass123',
            'name': 'Coach Name',
            'is_coach': True,
            'community_id': self.community.id,
        }
        res = self.client.post(CREATE_USER_URL, coach_payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=coach_payload['email'])
        self.assertTrue(user.check_password(coach_payload['password']))
        self.assertNotIn('password', res.data)

    def test_a03_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        res = self.client.post(CREATE_USER_URL, self.admin_payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a05_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test name',
            'community_id': self.community.id,
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_a07_create_token_for_user(self):
        """Test generates token for valid credentials."""
        res = self.client.post(TOKEN_URL, self.admin_payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_a09_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        self.admin_payload['password'] = 'badpass'
        res = self.client.post(TOKEN_URL, self.admin_payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a11_create_token_email_not_found(self):
        """Test error returned if user not found for given email."""
        payload = {'email': 'test@example.com', 'password': 'pass123', 'community_id': 1}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a13_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {'email': 'test@example.com', 'password': '', 'community_id': 1}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_a15_retrieve_user_unauthorized(self):
        """Test authentication is required for users."""
        unauthenticated_client = APIClient()
        res = unauthenticated_client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self) -> None:
        self.logger.setLevel(self.original_logging_level)


class B_PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        # print(self.user.__dict__)

    def test_b01_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get('name'), self.user.name)
        self.assertEqual(res.data.get('email'), self.user.email)

    def test_b03_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint."""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_b05_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {'name': 'Updated name', 'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
