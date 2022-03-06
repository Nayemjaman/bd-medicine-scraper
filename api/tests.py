from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from crawler.models import Medicine, Generic, Manufacturer


class MedicineDRFTests(APITestCase):
    def setUp(self):
        # Set up user
        self.user = User(username='testuser', email="foo@bar.com")
        password = 'test_password'
        self.user.set_password(password)
        self.user.save()
        token = Token.objects.create(user=self.user)
        token.save()

        # Authenticate client with user
        self.client = APIClient()
        # self.client.login(username=self.user.username, password=password)
        # self.client.force_login(self.user)
        # self.client.force_authenticate(user=self.user) # works

        self.medicine_data = {
            'brand_name': 'Napa',
            'generic': Generic.objects.create(generic_name='Test Generic'),
            'manufacturer': Manufacturer.objects.create(manufacturer_name='Test Manufacturer',
                                                        generics_count=1,
                                                        brand_names_count=1),
            'dosage_form': 'Test Dosage Form'
        }
        self.medicine = Medicine.objects.create(**self.medicine_data)

    def test_view_medicine(self):
        # https://stackoverflow.com/a/70697852/11105356
        self.client.force_authenticate(user=self.user)
        url = reverse('med_api:medicine-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
