from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from . models import CustomUser, Parking, Ticket, Area

from . serializers import CustomUserSerializer, AreaSerializer


AREA_URL = reverse('api:area-create-list')

CREATE_USER_URL = reverse('api:signup')
TOKEN_URL = reverse('api:signin')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


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


    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'username': 'test@londonappdev.com', 'email': 'test@londonappdev.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@londonappdev.com', password="testpass")
        payload = {'email': 'test@londonappdev.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class AdminAreaApiTests(TestCase):
    """Test the area API (admin)"""

    def setUp(self):
        self.client = APIClient()
        payload = {
            'email': 'test@amitpr.com',
            'password': 'testpass',
            'username': 'test@amitpr.com'
        }
        self.user = get_user_model().objects.create_user(**payload)
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse('api:area-create-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_retrieve_area_list(self):
        """Test retrieving a list of area"""
        Area.objects.create(capacity=100, name='Kale')
        Area.objects.create(capacity=200, name='Salt')

        res = self.client.get(AREA_URL)

        areas = Area.objects.all().order_by('-name')
        serializer = AreaSerializer(areas, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    




