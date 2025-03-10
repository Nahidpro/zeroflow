from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Package
import uuid 
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import serializers
from .serializers  import PackageSerializer
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import UserAccount 
from decimal import Decimal
from rest_framework.pagination import PageNumberPagination

User = get_user_model()
# class PackageModelTest(TestCase):
#     def setUp(self):
#         """
#         Set up a user and package instances for testing
#         """
#         self.user = get_user_model().objects.create_user(
#             username="testuser", password="testpassword"
#         )

#         # Create a package instance
#         self.package = Package.objects.create(
#             issued_by=self.user,
#             sender_name="Sender Name",
#             sender_address="Sender Address",
#             weight=10.0,
#             destination="City",
#             status="pending",
#             charge=100.0,
#             receiver_name="Receiver Name",
#             receiver_address="Receiver Address"
#         )

#     def test_generate_tracking_number(self):
#         """
#         Test that the tracking number is generated correctly.
#         """
#         package = Package.objects.create(
#             issued_by=self.user,
#             sender_name="Test Sender",
#             sender_address="Test Address",
#             weight=5.0,
#             destination="City",
#             status="pending",
#             charge=50.0,
#             receiver_name="Test Receiver",
#             receiver_address="Test Address"
#         )
#         tracking_number = package.tracking_number
#         date_prefix = timezone.now().strftime("%Y%m%d")
        

#         self.assertTrue(tracking_number.startswith(date_prefix))
#         self.assertEqual(len(tracking_number), 17)  

#     def test_package_soft_delete(self):
#         """
#         Test the soft_delete method marks the package as deleted.
#         """
#         self.package.soft_delete()

        
#         self.assertIsNotNone(self.package.deleted_at)
#         self.assertTrue(self.package.deleted_at <= timezone.now())

        
#         deleted_package = Package.deleted_packages.get(tracking_number=self.package.tracking_number)
#         self.assertEqual(deleted_package.tracking_number, self.package.tracking_number)

#     def test_package_restore(self):
#         """
#         Test the restore method correctly restores a soft-deleted package.
#         """
#         self.package.soft_delete()
#         self.package.restore()

     
#         self.assertIsNone(self.package.deleted_at)

        
#         restored_package = Package.active_packages.get(tracking_number=self.package.tracking_number)
#         self.assertEqual(restored_package.tracking_number, self.package.tracking_number)

#     def test_clean_method_delivered_status(self):
#         """
#         Test that when the status is 'delivered', the delivered_at field is populated.
#         """
#         self.package.status = 'delivered'
#         self.package.clean()

       
#         self.assertIsNotNone(self.package.delivered_at)
#         self.assertTrue(self.package.delivered_at <= timezone.now())

#     def test_clean_method_non_delivered_status(self):
#         """
#         Test that when the status is not 'delivered', the delivered_at field is None.
#         """
#         self.package.status = 'in_transit'
#         self.package.clean()

       
#         self.assertIsNone(self.package.delivered_at)

#     def test_package_save(self):
#         """
#         Test that the save method calls full_clean and saves the package.
#         """
       
#         self.package.save()
#         saved_package = Package.objects.get(tracking_number=self.package.tracking_number)
#         self.assertEqual(saved_package.status, self.package.status)
#         self.assertEqual(saved_package.tracking_number, self.package.tracking_number)





# class PackageCreateViewTests(TestCase):

#     def setUp(self):
#         self.client = APIClient()
#         self.user = UserAccount.objects.create_user(username='testuser', password='password') # Changed to UserAccount
#         self.client.force_authenticate(user=self.user)
#         self.create_url = reverse('package-create')
#         self.valid_data = {
#             'sender_name': 'New Sender',
#             'sender_address': 'New Sender Address',
#             'receiver_name': 'New Receiver',
#             'receiver_address': 'New Receiver Address',
#             'weight': 15.0,
#             'destination': 'New Destination',
#             'status': 'pending',
#             'charge': Decimal('0.00'),
#         }

#     def test_package_create_success(self):
#         response = self.client.post(self.create_url, self.valid_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Package.objects.count(), 1)
#         package = Package.objects.first()
#         self.assertEqual(package.sender_name, 'New Sender')
#         self.assertEqual(package.issued_by, self.user)

#     def test_package_create_invalid_data(self):
#         invalid_data = self.valid_data.copy()
#         invalid_data['weight'] = -1.0
#         response = self.client.post(self.create_url, invalid_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Package.objects.count(), 0)

#     def test_package_create_unauthenticated(self):
#         self.client.force_authenticate(user=None)
#         response = self.client.post(self.create_url, self.valid_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#         self.assertEqual(Package.objects.count(), 0)







# class PackageListViewTests(TestCase):

#     def setUp(self):
#         self.client = APIClient()
#         self.user = UserAccount.objects.create_user(username='testuser', password='password')
#         self.staff_user = UserAccount.objects.create_user(username='staffuser', password='password', is_staff=True)
#         self.client.force_authenticate(user=self.user)
#         self.list_url = reverse('package-list')

        
#         for i in range(5):
#             Package.objects.create(
#                 issued_by=self.user,
#                 sender_name=f'Sender {i}',
#                 sender_address=f'Address {i}',
#                 receiver_name=f'Receiver {i}',
#                 receiver_address=f'Receiver Address {i}',
#                 weight=10.0,
#                 destination=f'Destination {i}'
#             )
#         for i in range(3):
#             Package.objects.create(
#                 issued_by=self.staff_user,
#                 sender_name=f'Staff Sender {i}',
#                 sender_address=f'Staff Address {i}',
#                 receiver_name=f'Staff Receiver {i}',
#                 receiver_address=f'Staff Receiver Address {i}',
#                 weight=10.0,
#                 destination=f'Staff Destination {i}'
#             )

#     def test_package_list_authenticated_user(self):
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['results']['data']), 5)
#         self.assertEqual(response.data['count'], 5)

#     def test_package_list_staff_user(self):
#         self.client.force_authenticate(user=self.staff_user)
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data['results']['data']), 8)
#         self.assertEqual(response.data['count'], 8)

#     def test_package_list_unauthenticated(self):
#         self.client.force_authenticate(user=None)
#         response = self.client.get(self.list_url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    

# from django.utils import timezone

# class PackageDetailViewTests(TestCase):

#     def setUp(self):
#         self.client = APIClient()
#         self.user = UserAccount.objects.create_user(username='testuser', password='password')
#         self.staff_user = UserAccount.objects.create_user(username='staffuser', password='password', is_staff=True)
#         self.package = Package.objects.create(
#             issued_by=self.user,
#             sender_name='Sender Name',
#             sender_address='Sender Address',
#             receiver_name='Receiver Name',
#             receiver_address='Receiver Address',
#             weight=10.0,
#             destination='Destination'
#         )
#         self.detail_url = reverse('package-detail', kwargs={'tracking_number': self.package.tracking_number})
#         self.valid_data = {
#             'sender_name': 'New Sender',
#             'sender_address': 'New Sender Address',
#             'receiver_name': 'New Receiver',
#             'receiver_address': 'New Receiver Address',
#             'weight': 15.0,
#             'destination': 'New Destination',
#             'status': 'pending',
#             'charge': Decimal('0.00'),
#         }

#     def test_package_detail_authenticated_user(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.get(self.detail_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['data']['sender_name'], 'Sender Name')

    

#     def test_package_detail_unauthenticated(self):
#         response = self.client.get(self.detail_url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_package_update_authenticated_user(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.put(self.detail_url, self.valid_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['data']['sender_name'], 'New Sender')
#         self.package.refresh_from_db()
#         self.assertEqual(self.package.sender_name, 'New Sender')

#     def test_package_update_staff_user(self):
#         self.client.force_authenticate(user=self.staff_user)
#         response = self.client.put(self.detail_url, self.valid_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['data']['sender_name'], 'New Sender')
#         self.package.refresh_from_db()
#         self.assertEqual(self.package.sender_name, 'New Sender')

#     def test_package_update_unauthenticated(self):
#         response = self.client.put(self.detail_url, self.valid_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_package_update_permission_denied(self):
#         other_user = UserAccount.objects.create_user(username='otheruser', password='password')
#         self.client.force_authenticate(user=other_user)
#         response = self.client.put(self.detail_url, self.valid_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.package.refresh_from_db()
#         self.assertEqual(self.package.sender_name, 'Sender Name')

#     def test_package_update_partial(self):
#         self.client.force_authenticate(user=self.user)
#         partial_data = {'sender_name': 'Partial Update'}
#         response = self.client.patch(self.detail_url, partial_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['data']['sender_name'], 'Partial Update')
#         self.package.refresh_from_db()
#         self.assertEqual(self.package.sender_name, 'Partial Update')

#     def test_package_update_delivered_status(self):
#         self.client.force_authenticate(user=self.user)
#         data = {'status': 'delivered'}
#         response = self.client.patch(self.detail_url, data, format='json') 
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.package.refresh_from_db()
#         self.assertIsNotNone(self.package.delivered_at)



# class PackageDeleteViewTests(TestCase):

#     def setUp(self):
#         self.client = APIClient()
#         self.user = UserAccount.objects.create_user(username='testuser', password='password')
#         self.staff_user = UserAccount.objects.create_user(username='staffuser', password='password', is_staff=True)
#         self.package = Package.objects.create(
#             issued_by=self.user,
#             sender_name='Sender Name',
#             sender_address='Sender Address',
#             receiver_name='Receiver Name',
#             receiver_address='Receiver Address',
#             weight=10.0,
#             destination='Destination'
#         )
#         self.delete_url = reverse('package-delete', kwargs={'tracking_number': self.package.tracking_number})

#     def test_package_delete_authenticated_user(self):
#         self.client.force_authenticate(user=self.user)
#         response = self.client.delete(self.delete_url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.package.refresh_from_db()
#         self.assertIsNotNone(self.package.deleted_at)

#     def test_package_delete_staff_user(self):
#         self.client.force_authenticate(user=self.staff_user)
#         response = self.client.delete(self.delete_url)
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.package.refresh_from_db()
#         self.assertIsNotNone(self.package.deleted_at)

#     def test_package_delete_unauthenticated(self):
#         response = self.client.delete(self.delete_url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_package_delete_permission_denied(self):
#         other_user = UserAccount.objects.create_user(username='otheruser', password='password')
#         self.client.force_authenticate(user=other_user)
#         response = self.client.delete(self.delete_url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.package.refresh_from_db()
#         self.assertIsNone(self.package.deleted_at)

#     def test_package_delete_already_deleted(self):
#         self.package.soft_delete()
#         self.client.force_authenticate(user=self.user)
#         response = self.client.delete(self.delete_url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_package_delete_not_found(self):
#         self.client.force_authenticate(user=self.user)
#         non_existent_url = reverse('package-delete', kwargs={'tracking_number': 'nonexistent'})
#         response = self.client.delete(non_existent_url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from packages.models import Package
from accounts.models import UserAccount

class PackageRestoreViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = UserAccount.objects.create_user(username='testuser', password='password')
        self.staff_user = UserAccount.objects.create_user(username='staffuser', password='password', is_staff=True)
        self.package = Package.objects.create(
            issued_by=self.user,
            sender_name='Sender Name',
            sender_address='Sender Address',
            receiver_name='Receiver Name',
            receiver_address='Receiver Address',
            weight=10.0,
            destination='Destination'
        )
        self.package.soft_delete()  
        self.restore_url = reverse('package-restore', kwargs={'tracking_number': self.package.tracking_number})

    def test_package_restore_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.restore_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.package.refresh_from_db()
        self.assertIsNone(self.package.deleted_at)

    def test_package_restore_staff_user(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.put(self.restore_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.package.refresh_from_db()
        self.assertIsNone(self.package.deleted_at)

    def test_package_restore_unauthenticated(self):
        response = self.client.put(self.restore_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_package_restore_permission_denied(self):
        other_user = UserAccount.objects.create_user(username='otheruser', password='password')
        self.client.force_authenticate(user=other_user)
        response = self.client.put(self.restore_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.package.refresh_from_db()
        self.assertIsNotNone(self.package.deleted_at)

    def test_package_restore_not_found(self):
        self.client.force_authenticate(user=self.user)
        non_existent_url = reverse('package-restore', kwargs={'tracking_number': 'nonexistent'})
        response = self.client.put(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_package_restore_not_deleted(self):
        self.package.restore()
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.restore_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)