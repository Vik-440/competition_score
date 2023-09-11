"""Test for sports_person API."""

from django.contrib.auth import get_user_model
from django.test import TestCase
# from django.urls import reverse
from rest_framework.reverse import reverse

from rest_framework import status
from rest_framework.test import APIClient

from sports_person.models import SportsPerson

from sports_person.serializers import SportsPersonSerializer


# SPORTS_PERSON_URL = reverse('sports_person:sports_person-list')
SPORTS_PERSON_URL = reverse('sports_person:sportsperson-list')


def create_sports_person(**params):
    """Create and return a simple sports_person"""
    defaults = {
        'first_name': 'Kate',
        'last_name': 'Paradiuk',
        'birth_day': '2005-04-02',
        'rank': None,
        'city': 'Kyiv',
        'team': 'Junior',
    }
    defaults.update(params)

    sports_person = SportsPerson.objects.create(**defaults)
    return sports_person


# class PublicSportsPersonApiTests(TestCase):
#     """Test unauthenticated API requests."""

#     def setUp(self):
#         self.client = APIClient()

#     def test_auth_required(self):
#         """"Test auth is required to call API."""
#         res = self.client.get(SPORTS_PERSON_URL)

#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateSportsPersonApiTest(TestCase):
    """Test authenticate API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'pass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_sports_people(self):
        """Test retrieving a list of sports_people."""
        create_sports_person()
        create_sports_person()

        res = self.client.get(SPORTS_PERSON_URL)

        sports_people = SportsPerson.objects.all().order_by('-id')
        serializer = SportsPersonSerializer(sports_people, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_sports_person_api(self):
        """Test create one person"""
        sports_person = {
            'first_name': 'Kate',
            'last_name': 'Paradiuk',
            'birth_day': '2005-04-02',
            'rank': 'Masters',
            'city': 'Kyiv',
            'team': 'Junior',
        }

        res = self.client.post(SPORTS_PERSON_URL, sports_person, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        people = self.client.get(SPORTS_PERSON_URL)
        self.assertEqual(people.status_code, status.HTTP_200_OK)
        for person_data in people.json():
            del person_data['id']
            self.assertIn(person_data, [sports_person, ])
        # self.assertEqual(person_data, sports_person)

    def test_create_list_sports_people_api(self):
        """Test create list of people"""
        sports_people = [
            {
                'first_name': 'Kate',
                'last_name': 'Paradiuk',
                'birth_day': '2005-04-02',
                'rank': 'Masters',
                'city': 'Kyiv',
                'team': 'Junior',
            },
            {
                'first_name': 'Olga',
                'last_name': 'Test',
                'birth_day': '2000-08-05',
                'rank': 'Masters',
                'city': 'Lviv',
                'team': 'Angels',
            },
        ]

        res = self.client.post(SPORTS_PERSON_URL, sports_people, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        people = self.client.get(SPORTS_PERSON_URL)
        self.assertEqual(people.status_code, status.HTTP_200_OK)
        for person_data in people.json():
            del person_data['id']
            self.assertIn(person_data, sports_people)

    # def test_sports_person_list_limited_to_user(self):
    #     """Test list of sports_people is limited to auth user."""
    #     other_user = get_user_model().objects.create_user(
    #         'other@example.com',
    #         'pass321',
    #     )
    #     create_sports_person(user=other_user)
    #     create_sports_person(user=self.user)

    #     res = self.client.get(SPORTS_PERSON_URL)

    #     sports_people = SportsPerson.objects.filter(user=self.user)
    #     serializer = SportsPersonSerializer(sports_people, many=True)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)
