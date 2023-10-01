"""Test for judge_person API."""

from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from judge_person.models import JudgePerson
# from judge_person.serializers import JudgePersonSerializer


JUDGE_PERSON_URL = reverse('judge_person:judgeperson-list')
JUDGE_PERSON_1 = {
            'first_name': 'Natalia',
            'last_name': 'Blajko',
            'birth_day': '1990-06-02',
            'rank': 'Super Masters',
            'team': 'Angels',
            'license_expiration_date': '2025-01-01',
            'gender': None,
            'weight_kg': None,
            'height_cm': None,
        }
JUDGE_PERSON_2 = {
            'first_name': 'Olha',
            'last_name': 'Korobenko',
            'birth_day': '1990-01-12',
            'rank': 'Masters',
            'team': 'Junior',
            'license_expiration_date': '2023-01-01',
            'gender': None,
            'weight_kg': None,
            'height_cm': None,
        }


class PrivateJudgePersonApiTest(TestCase):
    """Test authenticated API requests in JudgePerson."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'pass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_judge_people(self):
        """Test retrieve a list of judge_person."""

        JudgePerson.objects.create(**JUDGE_PERSON_1)
        JudgePerson.objects.create(**JUDGE_PERSON_2)

        # res = self.client.post(
        #   JUDGE_PERSON_URL, judge_person_1, format='json')
        # self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(JUDGE_PERSON_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for judge_data in res.json()['results']:
            del judge_data['id']
            self.assertIn(judge_data, [JUDGE_PERSON_1, JUDGE_PERSON_2])

    def test_create_judge_post(self):
        """Create judge person by POST"""
        res = self.client.post(
            JUDGE_PERSON_URL,
            JUDGE_PERSON_1,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(JUDGE_PERSON_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for judge_data in res.json()['results']:
            del judge_data['id']
            self.assertIn(judge_data, [JUDGE_PERSON_1, ])

    def test_getting_judge_id(self):
        """Test retrieve Judge by ID"""
        res = self.client.post(
            JUDGE_PERSON_URL,
            JUDGE_PERSON_1,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(JUDGE_PERSON_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for judge_data in res.json()['results']:
            judge_id = judge_data.pop('id')
            self.assertIn(judge_data, [JUDGE_PERSON_1, ])

        JUDGE_PERSON_ID = f'{JUDGE_PERSON_URL}{judge_id}/'
        res = self.client.get(
            JUDGE_PERSON_ID
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.client.get(JUDGE_PERSON_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for judge_data in res.json()['results']:
            del judge_data['id']
            self.assertIn(judge_data, [JUDGE_PERSON_1, ])

    def test_retrieve_judge_by_query(self):
        """Test retrieve a list of judge_person by query search."""

        JudgePerson.objects.create(**JUDGE_PERSON_1)
        JudgePerson.objects.create(**JUDGE_PERSON_2)

        res = self.client.get(JUDGE_PERSON_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for judge_data in res.json()['results']:
            del judge_data['id']
            self.assertIn(judge_data, [JUDGE_PERSON_1, JUDGE_PERSON_2])

        search_part_data = {'last_name': 'aj'}
        res = self.client.get(JUDGE_PERSON_URL, search_part_data)
        res_judge = res.json()['results'][0]
        res_judge.pop('id')
        self.assertEqual(JUDGE_PERSON_1, res_judge)

        search_part_data = {'rank': 'up'}
        res = self.client.get(JUDGE_PERSON_URL, search_part_data)
        res_judge = res.json()['results'][0]
        res_judge.pop('id')
        self.assertEqual(JUDGE_PERSON_1, res_judge)

        search_part_data = {'team': 'io'}
        res = self.client.get(JUDGE_PERSON_URL, search_part_data)
        res_judge = res.json()['results'][0]
        res_judge.pop('id')
        self.assertEqual(JUDGE_PERSON_2, res_judge)

    def test_edit_judge_put(self):
        """Test for PUT Judge"""
        res = self.client.post(
            JUDGE_PERSON_URL,
            JUDGE_PERSON_1,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(JUDGE_PERSON_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for judge_data in res.json()['results']:
            judge_id = judge_data.pop('id')
            self.assertIn(judge_data, [JUDGE_PERSON_1, ])

        judge_person_edit = {
            'first_name': 'Natalia',
            'last_name': 'Blajko',
            'birth_day': '1990-06-02',
            'rank': 'Super Masters',
            'team': 'Angels',
            'license_expiration_date': '2025-01-01',
            'gender': None,
            'weight_kg': None,
            'height_cm': None,
        }
        JUDGE_PERSON_ID = f'{JUDGE_PERSON_URL}{judge_id}/'
        res = self.client.put(
            JUDGE_PERSON_ID,
            judge_person_edit,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.client.get(JUDGE_PERSON_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for judge_data in res.json()['results']:
            del judge_data['id']
            self.assertIn(judge_data, [judge_person_edit, ])

    def test_edit_judge_patch(self):
        """Test for PATCH Judge"""
        res = self.client.post(
            JUDGE_PERSON_URL,
            JUDGE_PERSON_1,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(JUDGE_PERSON_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for judge_data in res.json()['results']:
            judge_id = judge_data.pop('id')
            self.assertIn(judge_data, [JUDGE_PERSON_1, ])

        judge_person_edit = {
            'license_expiration_date': '2020-01-01',
        }
        JUDGE_PERSON_ID = f'{JUDGE_PERSON_URL}{judge_id}/'
        res = self.client.patch(
            JUDGE_PERSON_ID,
            judge_person_edit,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.client.get(JUDGE_PERSON_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for judge_data in res.json()['results']:
            self.assertEqual(
                judge_data['license_expiration_date'],
                judge_person_edit['license_expiration_date']
            )

    def test_delete_judge_id(self):
        """Test delete Judge by ID"""
        res = self.client.post(
            JUDGE_PERSON_URL,
            JUDGE_PERSON_1,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(JUDGE_PERSON_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for judge_data in res.json()['results']:
            judge_id = judge_data.pop('id')
            self.assertIn(judge_data, [JUDGE_PERSON_1, ])

        JUDGE_PERSON_ID = f'{JUDGE_PERSON_URL}{judge_id}/'
        res = self.client.delete(
            JUDGE_PERSON_ID
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        res = self.client.get(JUDGE_PERSON_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()['results'], [])

    def test_autocomplete_last_name(self):
        """Test autocomplete last_name field"""
        res = self.client.post(
            JUDGE_PERSON_URL,
            JUDGE_PERSON_1,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(JUDGE_PERSON_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for judge_data in res.json()['results']:
            del judge_data['id']
            self.assertIn(judge_data, [JUDGE_PERSON_1, ])

        JUDGE_PERSON_COMPLETE = f'{JUDGE_PERSON_URL}autocomplete_last_name/'
        part_autocomplete = {'last_name': 'aj'}
        autocomplete_last_name = self.client.get(
            JUDGE_PERSON_COMPLETE, part_autocomplete
        )
        self.assertEqual(
            autocomplete_last_name.data['auto_complete_last_name'], ['Blajko']
        )

    def test_autocomplete_rank(self):
        """Test autocomplete rank field"""
        res = self.client.post(
            JUDGE_PERSON_URL,
            JUDGE_PERSON_1,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(JUDGE_PERSON_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for judge_data in res.json()['results']:
            del judge_data['id']
            self.assertIn(judge_data, [JUDGE_PERSON_1, ])

        JUDGE_PERSON_COMPLETE = f'{JUDGE_PERSON_URL}autocomplete_ranks/'
        part_autocomplete = {'rank': 'up'}
        autocomplete_rank = self.client.get(
            JUDGE_PERSON_COMPLETE, part_autocomplete
        )
        self.assertEqual(
            autocomplete_rank.data['auto_complete_ranks'],
            ['Super Masters']
        )

    def test_retrieve_unique_ranks(self):
        """Test retrieve unique ranks"""
        res = self.client.post(
            JUDGE_PERSON_URL,
            JUDGE_PERSON_1,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(JUDGE_PERSON_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for judge_data in res.json()['results']:
            del judge_data['id']
            self.assertIn(judge_data, [JUDGE_PERSON_1, ])

        JUDGE_PERSON_UNIQUE = f'{JUDGE_PERSON_URL}get_unique_ranks/'
        unique_ranks = self.client.get(JUDGE_PERSON_UNIQUE)
        self.assertEqual(
            unique_ranks.data['unique_ranks'],
            ['Super Masters']
        )
