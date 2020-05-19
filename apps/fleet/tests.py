from django.contrib.auth.models import User
from django.test import TestCase

from apps.fleet.models import Vehicle


class AnimalTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='root', email='root@root.com', password='top_secret',
            is_superuser=True, is_staff=True)
        User.objects.create_user(
            username='simple', email='simple@simple.com', password='top_secret',
            is_staff=True)

    def test_root_user_can_create(self):
        """Animals that can speak are correctly identified"""
        root = User.objects.filter(username="root").first()
        vehicle = Vehicle.objects.create(name="Ford", registration="Ford123", brand="Chevrolet", type="Small",
                                         owner=root)
        self.assertIsInstance(vehicle, Vehicle)

    def test_simple_user_can_create(self):
        """Animals that can speak are correctly identified"""
        simple = User.objects.filter(username="simple").first()
        vehicle = Vehicle.objects.create(name="Gol", registration="Gol123", brand="Volkswagen", type="Small",
                                         owner=simple)
        self.assertIsInstance(vehicle, Vehicle)
