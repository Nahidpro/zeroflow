from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.serializers import UserRegistrationSerializer
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch 
from django.core.exceptions import ValidationError

UserAccount = get_user_model()
from django.test import TestCase
from django.contrib.auth import get_user_model

UserAccount = get_user_model()

### Model test
class UserAccountModelTests(TestCase):

    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'address': '123 Test St',
            'city': 'Test City',
            'zip_code': '12345',
            'phone_number': '1234567890',
            'first_name': 'Test',
            'last_name': 'User',
        }

    def test_create_user_account(self):
        user = UserAccount.objects.create_user(**self.user_data)

        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.address, self.user_data['address'])
        self.assertEqual(user.city, self.user_data['city'])
        self.assertEqual(user.zip_code, self.user_data['zip_code'])
        self.assertEqual(user.phone_number, self.user_data['phone_number'])

    def test_string_representation(self):
        user = UserAccount.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data['username'])

    def test_address_blank_null(self):
        user = UserAccount.objects.create_user(
            username='testuser_no_address',
            email='noaddress@example.com',
            password='testpassword'
        )
        self.assertIsNone(user.address)

    def test_city_blank_null(self):
        user = UserAccount.objects.create_user(
            username='testuser_no_city',
            email='nocity@example.com',
            password='testpassword'
        )
        self.assertIsNone(user.city)

    def test_zip_code_blank_null(self):
        user = UserAccount.objects.create_user(
            username='testuser_no_zip',
            email='nozip@example.com',
            password='testpassword'
        )
        self.assertIsNone(user.zip_code)

    def test_phone_number_blank_null(self):
        user = UserAccount.objects.create_user(
            username='testuser_no_phone',
            email='nophone@example.com',
            password='testpassword'
        )
        self.assertIsNone(user.phone_number)

    def test_max_length_city(self):
        long_city = "a" * 101
        user = UserAccount(
            username='testuser_long_city',
            email='longcity@example.com',
            password='testpassword',
            city=long_city
        )
        with self.assertRaises(ValidationError):
            user.full_clean() 
            user.save()

    def test_max_length_zip_code(self):
        long_zip = "1" * 21
        user = UserAccount(
            username='testuser_long_zip',
            email='longzip@example.com',
            password='testpassword',
            zip_code=long_zip
        )
        with self.assertRaises(ValidationError):
            user.full_clean()
            user.save()

    def test_max_length_phone_number(self):
        long_phone = "1" * 21
        user = UserAccount(
            username='testuser_long_phone',
            email='longphone@example.com',
            password='testpassword',
            phone_number=long_phone
        )
        with self.assertRaises(ValidationError):
            user.full_clean()
            user.save()


####### View test
class UserRegistrationSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123!",
            "password2": "TestPassword123!",
            "address": "123 Test Street",
            "city": "Test City",
            "zip_code": "12345",
            "phone_number": "1234567890",
            "first_name": "Test",
            "last_name": "User"
        }

        self.invalid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123!",
            "password2": "WrongPassword123!",
            "address": "123 Test Street",
            "city": "Test City",
            "zip_code": "12345",
            "phone_number": "1234567890",
            "first_name": "Test",
            "last_name": "User"
        }

    def test_serializer_with_valid_data(self):
        serializer = UserRegistrationSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, self.valid_data["username"])
        self.assertEqual(user.email, self.valid_data["email"])
        self.assertTrue(user.check_password(self.valid_data["password"]))

    def test_serializer_with_password_mismatch(self):
        serializer = UserRegistrationSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
        self.assertEqual(serializer.errors["password"][0], "Passwords do not match.")

class UserRegistrationViewAPITest(APITestCase):
    def setUp(self):
        self.url = reverse('user-registration')
        self.valid_payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123!",
            "password2": "TestPassword123!",
            "address": "123 Test Street",
            "city": "Test City",
            "zip_code": "12345",
            "phone_number": "1234567890",
            "first_name": "Test",
            "last_name": "User"
        }
        self.invalid_payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123!",
            "password2": "MismatchPassword!",
            "address": "123 Test Street",
            "city": "Test City",
            "zip_code": "12345",
            "phone_number": "1234567890",
            "first_name": "Test",
            "last_name": "User"
        }

    def test_registration_view_success(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "User registered successfully.")
        self.assertTrue(UserAccount.objects.filter(username="testuser").exists())

    def test_registration_view_failure(self):
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_duplicate_username_registration(self):
        self.client.post(self.url, self.valid_payload, format='json')
        duplicate_payload = self.valid_payload.copy()
        duplicate_payload['email'] = 'newemail@example.com'
        response = self.client.post(self.url, duplicate_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_duplicate_email_registration(self):
        self.client.post(self.url, self.valid_payload, format='json')
        duplicate_payload = self.valid_payload.copy()
        duplicate_payload['username'] = 'newuser'
        response = self.client.post(self.url, duplicate_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_missing_required_fields(self):
        missing_payload = self.valid_payload.copy()
        del missing_payload['password']
        response = self.client.post(self.url, missing_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email_format(self):
        invalid_email_payload = self.valid_payload.copy()
        invalid_email_payload['email'] = 'invalid_email'
        response = self.client.post(self.url, invalid_email_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_internal_server_error(self):
        with patch('accounts.views.UserRegistrationSerializer.save') as mock_save:
            mock_save.side_effect = Exception("Simulated error")
            response = self.client.post(self.url, self.valid_payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_correct_data_saved(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = UserAccount.objects.get(username=self.valid_payload['username'])
        self.assertEqual(user.email, self.valid_payload['email'])
        self.assertEqual(user.address, self.valid_payload['address'])
        self.assertEqual(user.city, self.valid_payload['city'])
        self.assertEqual(user.zip_code, self.valid_payload['zip_code'])
        self.assertEqual(user.phone_number, self.valid_payload['phone_number'])
        self.assertEqual(user.first_name, self.valid_payload['first_name'])
        self.assertEqual(user.last_name, self.valid_payload['last_name'])


class UserProfileUpdateViewTests(APITestCase):

    def setUp(self):
        self.url = reverse('user-profile-update')
        self.user = UserAccount.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            address='123 Test St',
            city='Test City',
            zip_code='12345',
            phone_number='1234567890',
        )
        self.client.force_authenticate(user=self.user)
        self.original_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'address': '123 Test St',
            'city': 'Test City',
            'zip_code': '12345',
            'phone_number': '1234567890',
        }
        self.updated_data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@example.com',
            'address': '456 Updated St',
            'city': 'Updated City',
            'zip_code': '67890',
            'phone_number': '0987654321',
        }

    def test_user_profile_update_success(self):
        response = self.client.patch(self.url, self.updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Profile updated successfully.')
        updated_user = UserAccount.objects.get(username=self.user.username)
        self.assertEqual(updated_user.first_name, self.updated_data['first_name'])
        self.assertEqual(updated_user.email, self.updated_data['email'])

    def test_user_profile_update_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.patch(self.url, self.updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_profile_update_duplicate_email(self):
        UserAccount.objects.create_user(
            username='otheruser',
            email='existing@example.com',
            password='testpassword'
        )
        self.updated_data['email'] = 'existing@example.com'
        response = self.client.patch(self.url, self.updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_profile_update_invalid_zip_code(self):
        self.updated_data['zip_code'] = 'invalidzip'
        response = self.client.patch(self.url, self.updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_profile_update_empty_data(self):
        response = self.client.patch(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Profile updated successfully.')

    def test_user_profile_update_no_change(self):
        response = self.client.patch(self.url, self.original_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Profile updated successfully.')
        updated_user = UserAccount.objects.get(username=self.user.username)
        self.assertEqual(updated_user.first_name, self.original_data['first_name'])
        self.assertEqual(updated_user.email, self.original_data['email'])