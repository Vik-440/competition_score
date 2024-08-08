"""Test for sports_person API."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.reverse import reverse

from rest_framework import status
from rest_framework.test import APIClient

from sports_person.models import SportsPerson

from sports_person.serializers import SportsPersonSerializer


SPORTS_PERSON_URL = reverse('sports_person:sportsperson-list')
PERSON_1 = {
    'first_name': 'Kate',
    'last_name': 'Paradiuk',
    'birth_day': '2005-04-02',
    'city': 'Kyiv',
    'team': 'Junior',
    'gender': None,
    'weight_kg': None,
    'height_cm': None,
}
PERSON_2 = {
    'first_name': 'Аріана',
    'last_name': 'Мішакова',
    'birth_day': '2000-08-05',
    'city': 'Київ',
    'team': 'Джуніор',
    'gender': 'female',
    'weight_kg': None,
    'height_cm': None,
}

def create_sports_person(**params):
    """Create and return a simple sports_person"""
    defaults = PERSON_1
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
        self.user = get_user_model().objects.create_superuser(
            'user@example.com',
            'pass123',
        )
        self.client.force_authenticate(self.user)

    def test_a01_retrieve_sports_people(self):
        """Test retrieving a list of sports_people."""
        create_sports_person()
        sports_people = SportsPerson.objects.all().order_by('-id')
        serializer = SportsPersonSerializer(sports_people, many=True)
        res = self.client.get(SPORTS_PERSON_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_a03_create_sports_person_api(self):
        """Test create one person"""
        res = self.client.post(SPORTS_PERSON_URL, PERSON_1, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        people = self.client.get(SPORTS_PERSON_URL)
        self.assertEqual(people.status_code, status.HTTP_200_OK)
        res_last_name = people.json()['results'][0]['last_name']
        self.assertEqual(res_last_name, PERSON_1['last_name'])

    def test_a05_create_list_sports_people_api(self):
        """Test create list of people"""
        sports_people = [PERSON_1, PERSON_2]
        res = self.client.post(SPORTS_PERSON_URL, sports_people, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        people = self.client.get(SPORTS_PERSON_URL)
        self.assertEqual(people.status_code, status.HTTP_200_OK)
        last_name_request = [person['last_name'] for person in sports_people]
        last_name_response = [
            person['last_name'] for person in people.json()['results']]
        self.assertEqual(last_name_request.sort(), last_name_response.sort())

    def test_a07_create_duplicate_sports_person_api(self):
        """Test create duplicate of person"""
        res = self.client.post(SPORTS_PERSON_URL, PERSON_1, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        sports_person_dup = PERSON_1
        res = self.client.post(
            SPORTS_PERSON_URL, sports_person_dup, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        people = self.client.get(SPORTS_PERSON_URL)
        self.assertEqual(people.status_code, status.HTTP_200_OK)
        res_last_name = people.json()['results'][0]['last_name']
        self.assertEqual(res_last_name, PERSON_1['last_name'])

    def test_a09_put_sports_person_api(self):
        """Test full change person"""
        res = self.client.post(SPORTS_PERSON_URL, PERSON_1, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        people = self.client.get(SPORTS_PERSON_URL)
        self.assertEqual(people.status_code, status.HTTP_200_OK)
        res_last_name = people.json()['results'][0]['last_name']
        self.assertEqual(res_last_name, PERSON_1['last_name'])
        person_id = people.json()['results'][0]['id']
        change_data = {
            'first_name': 'Kate',
            'last_name': 'Paradiuk',
            'birth_day': '2004-04-02',
            'rank': 'Masters',
            'city': 'Kyiv',
            'team': 'Junior',
            'gender': None,
            'weight_kg': None,
            'height_cm': None,
        }
        SPORTS_PERSON_ID = f'{SPORTS_PERSON_URL}{person_id}/'
        res = self.client.put(SPORTS_PERSON_ID, change_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        person_data = self.client.get(SPORTS_PERSON_ID)
        self.assertEqual(person_data.status_code, status.HTTP_200_OK)
        self.assertEqual(person_data.json()['birth_day'], '2004-04-02')

    def test_a11_patch_sports_person_api(self):
        """Test part change person"""
        res = self.client.post(SPORTS_PERSON_URL, PERSON_1, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        people = self.client.get(SPORTS_PERSON_URL)
        self.assertEqual(people.status_code, status.HTTP_200_OK)
        res_last_name = people.json()['results'][0]['last_name']
        self.assertEqual(res_last_name, PERSON_1['last_name'])
        person_id = people.json()['results'][0]['id']
        change_data = {
            'birth_day': '2004-04-02',
        }
        SPORTS_PERSON_ID = f'{SPORTS_PERSON_URL}{person_id}/'
        res = self.client.patch(SPORTS_PERSON_ID, change_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        person_data = self.client.get(SPORTS_PERSON_ID)
        self.assertEqual(person_data.status_code, status.HTTP_200_OK)
        self.assertEqual(person_data.json()['birth_day'], '2004-04-02')

    def test_a13_delete_sports_person_api(self):
        """Test delete person"""
        res = self.client.post(SPORTS_PERSON_URL, PERSON_1, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        people = self.client.get(SPORTS_PERSON_URL)
        self.assertEqual(people.status_code, status.HTTP_200_OK)
        res_last_name = people.json()['results'][0]['last_name']
        self.assertEqual(res_last_name, PERSON_1['last_name'])
        person_id = people.json()['results'][0]['id']
        SPORTS_PERSON_ID = f'{SPORTS_PERSON_URL}{person_id}/'
        res = self.client.delete(SPORTS_PERSON_ID)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        person_data = self.client.get(SPORTS_PERSON_ID)
        self.assertEqual(person_data.status_code, status.HTTP_404_NOT_FOUND)

    def test_a15_search_sports_person_api(self):
        """Test search by values person"""
        sports_people = [
            {
                'first_name': 'Kate',
                'last_name': 'Paradiuk',
                'birth_day': '2005-04-02',
                'rank': 'Masters',
                'city': 'Kyiv',
                'team': 'Junior',
                'gender': None,
                'weight_kg': None,
                'height_cm': None,
            },
            {
                'first_name': 'Ariana',
                'last_name': 'Mishakova',
                'birth_day': '2006-08-22',
                'rank': 'Pre_Masters',
                'city': 'Lviv',
                'team': 'Angels',
                'gender': None,
                'weight_kg': None,
                'height_cm': None,
            },
            {
                'first_name': 'Ulia',
                'last_name': 'Solovey',
                'birth_day': '2003-02-12',
                'rank': 'Coach',
                'city': 'Ujgorod',
                'team': 'Pigs',
                'gender': None,
                'weight_kg': None,
                'height_cm': None,
            },
            {
                'first_name': 'Anna',
                'last_name': 'Kozak',
                'birth_day': '2008-10-18',
                'rank': 'Junior',
                'city': 'Dnipro',
                'team': 'Birds',
                'gender': None,
                'weight_kg': None,
                'height_cm': None,
            }
        ]
        res = self.client.post(SPORTS_PERSON_URL, sports_people, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        people = self.client.get(SPORTS_PERSON_URL)
        self.assertEqual(people.status_code, status.HTTP_200_OK)
        last_name_request = [person['last_name'] for person in sports_people]
        last_name_response = [
            person['last_name'] for person in people.json()['results']]
        self.assertEqual(last_name_request.sort(), last_name_response.sort())
        search_part_data = {'last_name': 'koz'}
        res = self.client.get(SPORTS_PERSON_URL, search_part_data)
        res_person = res.json()['results'][0]['last_name']
        searched_person_last_name = 'Kozak'
        self.assertEqual(res_person, searched_person_last_name)

        search_part_data = {'team': 'Ang'}
        res = self.client.get(SPORTS_PERSON_URL, search_part_data)
        res_person = res.json()['results'][0]['last_name']
        searched_person_last_name = 'Mishakova'
        self.assertEqual(res_person, searched_person_last_name)
        search_part_data = {'city': 'ky'}
        res = self.client.get(SPORTS_PERSON_URL, search_part_data)
        res_person = res.json()['results'][0]['last_name']
        searched_person_last_name = 'Paradiuk'
        self.assertEqual(res_person, searched_person_last_name)

        search_part_data = {'born_after': '2008-10-10'}
        res = self.client.get(SPORTS_PERSON_URL, search_part_data)
        res_person = res.json()['results'][0]['last_name']
        searched_person_last_name = 'Kozak'
        self.assertEqual(res_person, searched_person_last_name)

        search_part_data = {'born_before': '2003-02-15'}
        res = self.client.get(SPORTS_PERSON_URL, search_part_data)
        res_person = res.json()['results'][0]['last_name']
        searched_person_last_name = 'Solovey'
        self.assertEqual(res_person, searched_person_last_name)

    def test_a17_get_unique_data_api(self):
        """Test getting unique teams, cities, ranks"""
        sports_people = [
            {
                'first_name': 'Kate',
                'last_name': 'Paradiuk',
                'birth_day': '2005-04-02',
                'rank': 'Masters',
                'city': 'Kyiv',
                'team': 'Junior',
                'gender': None,
                'weight_kg': None,
                'height_cm': None,
            },
            {
                'first_name': 'Ariana',
                'last_name': 'Mishakova',
                'birth_day': '2006-08-22',
                'rank': 'Pre_Masters',
                'city': 'Lviv',
                'team': 'Angels',
                'gender': None,
                'weight_kg': None,
                'height_cm': None,
            },
            {
                'first_name': 'Anna',
                'last_name': 'Kozak',
                'birth_day': '2008-10-18',
                'rank': 'Junior',
                'city': 'Dnipro',
                'team': 'Birds',
                'gender': None,
                'weight_kg': None,
                'height_cm': None,
            },
            {
                'first_name': 'Ulia',
                'last_name': 'Solovey',
                'birth_day': '2003-02-12',
                'rank': 'Coach',
                'city': 'Ujgorod',
                'team': 'Pigs',
                'gender': None,
                'weight_kg': None,
                'height_cm': None,
            }
        ]

        res = self.client.post(SPORTS_PERSON_URL, sports_people, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        people = self.client.get(SPORTS_PERSON_URL)
        self.assertEqual(people.status_code, status.HTTP_200_OK)
        last_name_request = [person['last_name'] for person in sports_people]
        last_name_response = [
            person['last_name'] for person in people.json()['results']]
        self.assertEqual(last_name_request.sort(), last_name_response.sort())
        unique_cities_url = f'{SPORTS_PERSON_URL}get_unique_cities/'
        unique_cities = self.client.get(unique_cities_url)
        cities = sorted([person['city'] for person in sports_people])
        self.assertEqual(sorted(unique_cities.data['unique_cities']), cities)
        unique_teams_url = f'{SPORTS_PERSON_URL}get_unique_teams/'
        unique_teams = self.client.get(unique_teams_url)
        teams = sorted([person['team'] for person in sports_people])
        self.assertEqual(sorted(unique_teams.data['unique_teams']), teams)

    def test_a19_autocomplete_data_api(self):
        """Test autocomplete fields for teams, cities, ranks"""
        sports_people = [
            {
                'first_name': 'Kate',
                'last_name': 'Paradiuk',
                'birth_day': '2005-04-02',
                'rank': 'Masters',
                'city': 'Kyiv',
                'team': 'Junior',
                'gender': None,
                'weight_kg': None,
                'height_cm': None,
            },
            {
                'first_name': 'Ariana',
                'last_name': 'Mishakova',
                'birth_day': '2006-08-22',
                'rank': 'Pre_Masters',
                'city': 'Lviv',
                'team': 'Angels',
                'gender': None,
                'weight_kg': None,
                'height_cm': None,
            },
            {
                'first_name': 'Anna',
                'last_name': 'Kozak',
                'birth_day': '2008-10-18',
                'rank': 'Junior',
                'city': 'Dnipro',
                'team': 'Birds',
                'gender': None,
                'weight_kg': None,
                'height_cm': None,
            },
            {
                'first_name': 'Ulia',
                'last_name': 'Solovey',
                'birth_day': '2003-02-12',
                'rank': 'Coach',
                'city': 'Ujgorod',
                'team': 'Pigs',
                'gender': None,
                'weight_kg': None,
                'height_cm': None,
            }
        ]

        res = self.client.post(SPORTS_PERSON_URL, sports_people, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        part_autocomplete = {'city': 'lv'}
        autocomplete_cities_url = f'{SPORTS_PERSON_URL}autocomplete_cities/'
        autocomplete_cities = self.client.get(
            autocomplete_cities_url, part_autocomplete)
        self.assertEqual(
            autocomplete_cities.data['auto_complete_cities'], ['Lviv'])

        part_autocomplete = {'team': 'an'}
        autocomplete_teams_url = f'{SPORTS_PERSON_URL}autocomplete_teams/'
        autocomplete_teams = self.client.get(
            autocomplete_teams_url, part_autocomplete)
        self.assertEqual(
            autocomplete_teams.data['auto_complete_teams'], ['Angels'])

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
