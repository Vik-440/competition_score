"""Test for Squad Person API."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
# from unittest import TestCase

# from sports_person.models import SportsPerson

RANK_URL = reverse('sports_person:personrank-list')
SPORTS_PERSON_URL = reverse('sports_person:sportsperson-list')
COMPETITION_URL = reverse('competition:competition-list')
NOMINATION_URL = reverse('nomination:nomination-list')
CONDITION_PER_URL = reverse('nomination:conditionperformance-list')
SQUAD_URL = reverse('squad:squad-list')
SQUAD_PERSON_URL = reverse('squad_person:squadperson-list')

RANK_1 = {
    'person_rank_name': 'Junior',
    'person_rank_weight': 50,
}
RANK_2 = {
    'person_rank_name': 'Master',
    'person_rank_weight': 80,
}
RANK_3 = {
    'person_rank_name': 'Super Master',
    'person_rank_weight': 90,
}
PERSON_1 = {
    'first_name': 'Kate',
    'last_name': 'Paradiuk',
    'birth_day': '2005-04-02',
    'person_rank_id': 3,
    'city': 'Kyiv',
    'team': 'Junior',
    'gender': 'female',
    'weight_kg': 55,
    'height_cm': 168,
}
PERSON_2 = {
    'first_name': 'Ariana',
    'last_name': 'Mishakova',
    'birth_day': '2005-09-22',
    'person_rank_id': 2,
    'city': 'Lviv',
    'team': 'Angels',
    'gender': 'female',
    'weight_kg': 65,
    'height_cm': 179,
}
COMPETITION = {
  "competition_name": "Cup autumn 2023",
  "competition_city": "Lviv",
  "competition_date": "2023-11-11",
  "competition_qty_days": 2
}
NOMINATION_1 = {
    'nomination_name': 'Dance 8-12 y.o.',
    'nomination_start_date_time': '2023-11-11T08:00',
    'performance_second': 120,
    'delay_between_performance_second': 60,
    'competition_id': 444,
}
CONDITION_PER_1 = {
    'men_person': True,
    'women_person': True,
    'min_qty_person': 1,
    'max_qty_person': 2,
    'min_age_person': None,
    'max_age_person': 62,
    'min_weight_person': 15,
    'max_weight_person': 86,
    'min_height_person': 22,
    'max_height_person': 211,
    'nomination_id': 1,
    'min_rank_person': 'Junior',
    'max_rank_person': 'Super Master',
}
SQUAD_1 = {
    'squad_name': 'Junior Barbie 8-12 y.e.',
    'performance_date_time': '2023-11-11T12:23:00',
    'nomination_id': 1,
}
SQUAD_PERSON_1 = {
    'squad_id': 1,
    'sports_person_id': 1
}
SQUAD_PERSON_2 = {
    'squad_id': 1,
    'sports_person_id': 2
}

"""Need test qty person in squad"""


class SquadPersonApiTest(TestCase):
    """Test API around SquadPerson."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            'user@example.com',
            'pass123',
        )
        self.client.force_authenticate(self.user)

    def create_rank(self, rank: dict) -> None:
        """Create simple rank."""
        result = self.client.post(RANK_URL, rank, format='json')
        if result.status_code != status.HTTP_201_CREATED:
            print(result.json())
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        rank_get = self.client.get(RANK_URL)
        self.assertEqual(rank_get.status_code, status.HTTP_200_OK)
        print('\ntest create rank - OK')
        return None

    def create_sport_person(self, person: dict) -> None:
        """Create a simple sport_person."""
        result = self.client.post(SPORTS_PERSON_URL, person, format='json')
        if result.status_code != status.HTTP_201_CREATED:
            print(result.json())
        person_id = result.json()['id']
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        person_get = self.client.get(SPORTS_PERSON_URL)
        self.assertEqual(person_get.status_code, status.HTTP_200_OK)
        person_name = person_get.json()['results'][0]['last_name']
        self.assertEqual(person_name, person['last_name'])
        print('test create person - OK')
        return person_id

    def create_competition(self) -> None:
        """Create a simple competition"""
        result = self.client.post(COMPETITION_URL, COMPETITION, format='json')
        if result.status_code != status.HTTP_201_CREATED:
            print(result.json())
        competition_id = result.json()['id']
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        competition_get = self.client.get(COMPETITION_URL)
        self.assertEqual(competition_get.status_code, status.HTTP_200_OK)
        competition_name = (
            competition_get.json()['results'][0]['competition_name'])
        self.assertEqual(competition_name, COMPETITION['competition_name'])
        print('test create competition - OK')
        return competition_id

    def create_nomination(self, competition_id) -> None:
        """Create a simple nomination."""
        NOMINATION_1.update({'competition_id': competition_id})
        result = self.client.post(NOMINATION_URL, NOMINATION_1, format='json')
        if result.status_code != status.HTTP_201_CREATED:
            print(result.json())
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        nomination_get = self.client.get(NOMINATION_URL)
        self.assertEqual(nomination_get.status_code, status.HTTP_200_OK)
        nomination_name = (
            nomination_get.json()['results'][0]['nomination_name'])
        self.assertEqual(nomination_name, NOMINATION_1['nomination_name'])
        print('test create nomination - OK')
        return None

    def create_condition_performance(self) -> None:
        """Create conditions for the nomination."""
        result = self.client.post(
            CONDITION_PER_URL, CONDITION_PER_1, format='json')
        if result.status_code != status.HTTP_201_CREATED:
            print(result.json())
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        condition_get = self.client.get(CONDITION_PER_URL)
        self.assertEqual(condition_get.status_code, status.HTTP_200_OK)
        condition_bind = (
            condition_get.json()['results'][0]['nomination_id'])
        self.assertEqual(condition_bind, CONDITION_PER_1['nomination_id'])
        print('test create condition performance - OK')
        return None

    def create_squad(self) -> None:
        """Create squad under nomination"""
        result = self.client.post(SQUAD_URL, SQUAD_1, format='json')
        if result.status_code != status.HTTP_201_CREATED:
            print(result.json())
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        squad_get = self.client.get(SQUAD_URL)
        self.assertEqual(squad_get.status_code, status.HTTP_200_OK)
        squad_bind = squad_get.json()['results'][0]['nomination_id']
        self.assertEqual(squad_bind, SQUAD_1['nomination_id'])
        print('test create squad - OK')
        return None

    def create_squad_person(self, sq_person: dict, person_id: int) -> None:
        """Create a simple squad_person"""
        sq_person.update({'sports_person_id': person_id})
        result = self.client.post(
            SQUAD_PERSON_URL, sq_person, format='json')
        if result.status_code != status.HTTP_201_CREATED:
            print(result.json())
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        squad_person_get = self.client.get(SQUAD_PERSON_URL)
        self.assertEqual(squad_person_get.status_code, status.HTTP_200_OK)
        squad_person_much = squad_person_get.json()['results'][0]['squad_id']
        self.assertEqual(squad_person_much, sq_person['squad_id'])
        print('test create squad_person - OK')
        return None

    def test_create_rank_person_competition_nomination_condition_squad_squadperson_api(self): # noqa
        """
        Create step by step all components for testing SquadPerson under
        conditions from nomination in general.
        """
        self.create_rank(RANK_1)
        self.create_rank(RANK_2)
        self.create_rank(RANK_3)

        person_1_id = self.create_sport_person(PERSON_1)
        person_2_id = self.create_sport_person(PERSON_2)

        competition_id = self.create_competition()

        self.create_nomination(competition_id)

        self.create_condition_performance()

        self.create_squad()

        self.create_squad_person(SQUAD_PERSON_1, person_1_id)
        self.create_squad_person(SQUAD_PERSON_2, person_2_id)
