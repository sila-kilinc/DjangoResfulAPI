from django.test import TestCase
from ..models import AddUser


class UserTest(TestCase):
    """ Test module for adduser model """

    def setUp(self):
        AddUser.objects.create(
            username='Leo', email='leo@gmail.com', job='Engineer', age='24')
        AddUser.objects.create(
            username='Melis', email='melis@gmail.com', job='Doctor', age='28')
        AddUser.objects.create(
            username='Daniel', email='daniel@gmail.com', job='Nurse', age='23')
        AddUser.objects.create(
            username='Julie', email='julie@gmail.com', job='Designer', age='42')

    def test_user_email(self):
        leo = AddUser.objects.get(username='Leo')
        melis = AddUser.objects.get(username='Melis')
        daniel = AddUser.objects.get(username='Daniel')
        julie = AddUser.objects.get(username='Julie')
        self.assertEqual(
            leo.get_email(), 'leo@gmail.com')
        self.assertEqual(
            melis.get_email(), 'melis@gmail.com')
        self.assertEqual(
            daniel.get_email(), 'daniel@gmail.com')
        self.assertEqual(
            julie.get_email(), 'julie@gmail.com')
