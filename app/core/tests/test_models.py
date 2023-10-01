"""Tests for models."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from sports_person.models import SportsPerson


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user an email is successful."""
        email = 'test@example.com'
        password = 'test_pass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_sports_person(self):
        """Tests create DB sports person."""
        first_name = 'Катерина'
        team_tmp = 'Джуніор'
        city = 'Тернопіль'
        team = team_tmp
        person = SportsPerson.objects.create(
            first_name=first_name,
            last_name='Парадюк',
            birth_day='2005-04-02',
            city=city,
            team=team,
            # person_rank_id=1,
        )

        self.assertEqual(person.id, 1)
        self.assertEqual(person.first_name, first_name)
        self.assertEqual(SportsPerson.objects.get(id=1).team, team)
        self.assertEqual(SportsPerson.objects.get(
            first_name=first_name).team, team)
        self.assertEqual(SportsPerson.objects.get(
            first_name='Катерина').team, team)
