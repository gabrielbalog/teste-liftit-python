from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.fleet.models import Vehicle


class VehicleTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='root', email='root@root.com', password='top_secret',
            is_superuser=True, is_staff=True)
        User.objects.create_user(
            username='simple', email='simple@simple.com', password='top_secret',
            is_staff=True)

    def test_root_user_can_create(self):
        """Superuser can create a vehicle"""
        root = User.objects.filter(username="root").first()
        vehicle = Vehicle.objects.create(name="Ford", registration="Ford123", brand="Chevrolet", type="Small",
                                         owner=root)
        self.assertIsInstance(vehicle, Vehicle)

    def test_simple_user_can_create(self):
        """Simple user can create a vehicle"""
        simple = User.objects.filter(username="simple").first()
        vehicle = Vehicle.objects.create(name="Gol", registration="Gol123", brand="Volkswagen", type="Small",
                                         owner=simple)
        self.assertIsInstance(vehicle, Vehicle)


class VehicleAPITestCase(APITestCase):
    def setUp(self):
        self.root = User.objects.create_user(
            username='root', email='root@root.com', password='top_secret',
            is_superuser=True, is_staff=True)
        self.user = User.objects.create_user(
            username='simple', email='simple@simple.com', password='top_secret',
            is_staff=True)
        Token.objects.create(user=self.user)

    def _autheticate_client(self):
        token = Token.objects.get(user__username='simple')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_vehicle_unauthorized(self):
        """
        Not allow unauthorized access to create vehicle
        """
        data = {'name': 'Ford'}
        response = self.client.post('/fleet/vehicle/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_vehicle_incomplete(self):
        """
        Ensure that only fully data is accepted to create vehicle
        """
        self._autheticate_client()
        data = {'name': 'Ford'}
        response = self.client.post('/fleet/vehicle/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_vehicle_complete(self):
        """
        Ensure that fully data is able to create a vehicle
        """
        self._autheticate_client()
        data = {'name': 'Ford', 'registration': 'f1', 'brand': 'Chrvolet', 'type': 'small', 'owner': self.user.id}
        response = self.client.post('/fleet/vehicle/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        return response.data.get('id')

    def test_retrieve_vehicle_unauthorized(self):
        """
        Not allow to retrieve data without authentication
        """
        _id = self.test_create_vehicle_complete()
        self.client.credentials()

        response = self.client.get(f'/fleet/vehicle/{_id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_vehicle(self):
        """
        Ensure we can retrieve a vehicle
        """
        self._autheticate_client()
        _id = self.test_create_vehicle_complete()

        response = self.client.get(f'/fleet/vehicle/{_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {'id': _id, 'name': 'Ford', 'registration': 'f1', 'brand': 'Chrvolet', 'type': 'small',
                          'owner': self.user.id})

    def test_retrieve_vehicles_unauthorized(self):
        """
        Not allow to retrieve data without authentication
        """
        self.client.credentials()

        response = self.client.get('/fleet/vehicle/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_vehicles(self):
        """
        Ensure we can retrieve vehicles
        """
        self._autheticate_client()
        self.test_create_vehicle_complete()

        response = self.client.get('/fleet/vehicle/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_vehicle(self):
        """
        Ensure we can update a vehicle.
        """
        self._autheticate_client()
        _id = self.test_create_vehicle_complete()
        data = {'name': 'Gol', 'registration': 'g1', 'brand': 'Volkswagen', 'type': 'small', 'owner': self.user.id}

        response = self.client.put(f'/fleet/vehicle/{_id}/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {'id': _id, 'name': 'Gol', 'registration': 'g1', 'brand': 'Volkswagen', 'type': 'small',
                          'owner': self.user.id})

    def test_delete_vehicle(self):
        """
        Ensure we can delete a vehicle.
        """
        self._autheticate_client()
        _id = self.test_create_vehicle_complete()

        response = self.client.delete(f'/fleet/vehicle/{_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_see_only_my_vehicles(self):
        """
        Ensure that only user vehicle is returned
        Ensure that not only users' vehicle is avaiable
        """
        for i in range(5):
            Vehicle.objects.create(
                name=f"root{i}",
                registration=f"registration{i}",
                brand=f"brand{i}",
                type=f"type{i}",
                owner=self.root,
            )

        for i in range(5):
            Vehicle.objects.create(
                name=f"simple{i}",
                registration=f"registration{i}",
                brand=f"brand{i}",
                type=f"type{i}",
                owner=self.user,
            )

        self._autheticate_client()

        response = self.client.get(f'/fleet/vehicle/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(Vehicle.objects.all().count(), 10)
