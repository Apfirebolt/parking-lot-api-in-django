from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from . models import Area
from . serializers import AreaSerializer


CREATE_USER_URL = reverse('api:signup')
TOKEN_URL = reverse('api:signin')
ME_URL = reverse('api:me')
AREA_URL = reverse('api:area-create-list')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            'test@londonappdev.com',
            'someusername',
            'testpass'
        )
        self.client.force_authenticate(self.user)
        
    def test_logged_in_user(self):
        response = self.client.get(reverse('api:me'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@amitpr.com',
            'username': 'Test username',
            'password': 'testpass',
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
            'username': 'Test username',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'test@amitpr.com',
            'password': 'pw',
            'username': 'Test',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@amitpr.com', username='Test User', password="testpass")
        payload = {'email': 'test@amitpr.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_retrieve_area_list(self):
        """Test retrieving a list of areas"""
        Area.objects.create(capacity=10, name='Kale')
        Area.objects.create(capacity=20, name='Salt')

        res = self.client.get(AREA_URL)

        areas = Area.objects.all()
        serializer = AreaSerializer(areas, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    
    def test_create_area_successful(self):
        """Test create a new area"""
        payload = {'capacity': 200, 'name': 'Cabbage'}
        self.client.post(AREA_URL, payload)

        exists = Area.objects.filter(
            capacity=payload['capacity'],
            name=payload['name'],
        ).exists()
        self.assertTrue(exists)