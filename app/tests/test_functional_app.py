"""Functional test the all app in general."""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status

from rest_framework.test import APIClient

import logging

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_superuser(**params) -> object:
    """Create superuser."""
    return get_user_model().objects.create_superuser(**params)

# def create_admin(**params) -> object:
#     """Create admin for separate community"""
#     return get_user_model().objects.create_admin(**params)


class A_01_StartingWorkInAppTest(TestCase):
    """checking readiness for the first launch of the project."""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.superuser_payload = {
            'email': 'superuser@cs.com',
            'password': 'superuser123'
        }
        cls.superuser = create_superuser(**cls.superuser_payload)

    def setUp(self) -> None:
        self.client_superuser = APIClient()
        self.client_superuser.force_authenticate(user=self.superuser)

    def test_a_00_superuser_is_created(self):
        """test - superuser is created and authenticated"""
        self.assertIsNotNone(self.superuser)
        self.assertTrue(self.superuser.is_superuser)

    def test_a_05_create_new_community_for_client(self):
        None
