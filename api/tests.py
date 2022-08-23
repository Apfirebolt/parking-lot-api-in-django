from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from . models import CustomUser, Parking, Ticket, Area

from . serializers import CustomUserSerializer


AREA_URL = reverse('api:area-create-list')

CREATE_USER_URL = reverse('api:signup')
TOKEN_URL = reverse('api:signin')


def create_user(**params):
    return CustomUser.objects.create(**params)


class PublicAreaApiTests(TestCase):
    """Test only authenticated users can access to Area URL"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(AREA_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@amitpr.com',
            'password': 'testpass',
            'username': 'Testusername'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {
            'email': 'test@amitpr.com',
            'password': 'testpass',
            'username': 'Testusername',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)




