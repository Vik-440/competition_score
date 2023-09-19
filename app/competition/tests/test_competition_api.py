"""Test for competition API."""

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


COMPETITION_URL = reverse('competition:competition-list')


class PrivateCompetitionApiTest(TestCase):
    """Test authenticated API request in Competition."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'pass123',
        )
        self.client.force_authenticate(self.user)

    def test_create_retrieve_competition(self):
        """Test for testing GET, POST, PUT, PATCH, DELETE methods"""
        performance = {
            'competition_name': 'Lviv Cup 2023',
            'competition_city': 'Lviv',
            'competition_date': '2023-10-10',
            'competition_qty_days': 2,
        }
        res = self.client.post(COMPETITION_URL, performance, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(COMPETITION_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()['results'][0]
        competition_id = res_data.pop('id')
        self.assertEqual(res_data, performance)

        performance_new = {
            'competition_name': 'Lviv Cup 2023',
            'competition_city': 'Lviv',
            'competition_date': '2023-10-10',
            'competition_qty_days': 3,
        }
        COMPETITION_ID = f'{COMPETITION_URL}{competition_id}/'
        res = self.client.put(COMPETITION_ID, performance_new, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.client.get(COMPETITION_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()['results'][0]
        del res_data['id']
        self.assertEqual(res_data, performance_new)

        performance_new = {
            'competition_qty_days': 4,
        }
        res = self.client.patch(COMPETITION_ID, performance_new, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.client.get(COMPETITION_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()['results'][0]['competition_qty_days']
        self.assertEqual(res_data, 4)

        res = self.client.delete(COMPETITION_ID)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        res = self.client.get(COMPETITION_ID)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_by_query(self):
        """Testing searching by query params"""
        performance_1 = {
            'competition_name': 'Lviv Cup 2023',
            'competition_city': 'Lviv',
            'competition_date': '2023-10-10',
            'competition_qty_days': 2,
        }
        res = self.client.post(COMPETITION_URL, performance_1, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        performance_2 = {
            'competition_name': 'Kyiv Cup 2024',
            'competition_city': 'Kyiv',
            'competition_date': '2024-11-11',
            'competition_qty_days': 3,
        }
        res = self.client.post(COMPETITION_URL, performance_2, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(COMPETITION_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 2)

        part_search = {'competition_name': '2023'}
        res = self.client.get(COMPETITION_URL, part_search)
        res_data = res.data['results'][0]
        del res_data['id']
        self.assertEqual(res_data, performance_1)

        part_search = {'competition_city': 'Ky'}
        res = self.client.get(COMPETITION_URL, part_search)
        res_data = res.data['results'][0]
        del res_data['id']
        self.assertEqual(res_data, performance_2)

        part_search = {'date_period_start': '2024-01-01'}
        res = self.client.get(COMPETITION_URL, part_search)
        res_data = res.data['results'][0]
        del res_data['id']
        self.assertEqual(res_data, performance_2)

        part_search = {'date_period_end': '2024-01-01'}
        res = self.client.get(COMPETITION_URL, part_search)
        res_data = res.data['results'][0]
        del res_data['id']
        self.assertEqual(res_data, performance_1)
