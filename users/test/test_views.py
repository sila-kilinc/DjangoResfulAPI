import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import AddUser

from ..serializers import UserSerializer

# initialize the APIClient app
client = Client()


# Tests for Django Restful Api
class GetAllUserTest(TestCase):
    """ Test module for GET all user API """

    def setUp(self):
        AddUser.objects.create(
            username='Leo', email='leo@gmail.com', job='Engineer', age='24')
        AddUser.objects.create(
            username='Melis', email='melis@gmail.com', job='Doctor', age='28')
        AddUser.objects.create(
            username='Daniel', email='daniel@gmail.com', job='Nurse', age='23')
        AddUser.objects.create(
            username='Julie', email='julie@gmail.com', job='Designer', age='42')

    def test_get_all_users(self):
        # get API response
        response = client.get(reverse('get_post_user'))
        # get data from db
        users = AddUser.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleUserTest(TestCase):
    """ Test module for GET single user API """

    def setUp(self):
        self.user = AddUser.objects.create(
            username='Leo', email='leo@gmail.com', job='Engineer', age='24')
        self.user2 = AddUser.objects.create(
            username='Melis', email='melis@gmail.com', job='Doctor', age='28')
        self.user3 = AddUser.objects.create(
            username='Daniel', email='daniel@gmail.com', job='Nurse', age='23')
        self.user4 = AddUser.objects.create(
            username='Julie', email='julie@gmail.com', job='Designer', age='42')

    def test_get_valid_single_user(self):
        # Test for valid user.
        response = client.get(
            reverse('get_put_delete', kwargs={'user_id': self.user2.id}))
        user = AddUser.objects.get(id=self.user2.id)
        serializer = UserSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_user(self):
        #  Test for invalid user.
        response = client.get(
            reverse('get_put_delete', kwargs={'user_id': 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewUserTest(TestCase):
    """ Test module for inserting a new user """

    def setUp(self):
        self.valid_payload = {
            'username': 'Leo',
            'email': 'leo@gmail.com',
            'job': 'Engineer',
            'age': '24',

        }
        self.invalid_payload = {
            'username': '',
            'email': 'leo@gmail.com',
            'job': 'Engineer',
            'age': '24',
        }

    def test_create_valid_user(self):
        response = client.post(
            reverse('get_post_user'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        response = client.post(
            reverse('get_post_user'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleUserTest(TestCase):
    """ Test module for updating an existing user record """

    def setUp(self):
        self.user = AddUser.objects.create(
            username='Leo', email='leo@gmail.com', job='Engineer', age='24')
        self.user2 = AddUser.objects.create(
            username='Melis', email='melis@gmail.com', job='Doctor', age='28')
        self.valid_payload = {
            'username': 'Melis',
            'email': 'leos@gmail.com',
            'job': 'Developer',
            'age': '29',
        }
        self.invalid_payload = {
            'username': '',
            'email': 'melisis@gmail.com',
            'job': 'ProfDoctor',
            'age': '30',
        }

    def test_valid_update_user(self):
        response = client.put(
            reverse('get_put_delete', kwargs={'user_id': self.user2.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_user(self):
        response = client.put(
            reverse('get_put_delete', kwargs={'user_id': self.user2.id}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleUserTest(TestCase):
    """ Test module for deleting an existing user record """

    def setUp(self):
        self.user = AddUser.objects.create(
            username='Leo', email='leo@gmail.com', job='Engineer', age='24')
        self.user2 = AddUser.objects.create(
            username='Melis', email='melis@gmail.com', job='Doctor', age='28')

    def test_valid_delete_user(self):
        response = client.delete(
            reverse('get_put_delete', kwargs={'user_id': self.user2.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_user(self):
        response = client.delete(
            reverse('get_put_delete', kwargs={'user_id': 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
