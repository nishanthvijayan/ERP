"""Test cases for Purchase Home, My Submissions, Pending Requests, Previous Requests pages."""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

from erp_core.models import Address, Department, Pay


class PurchaseAllApprovedViewTests(TestCase):
    """Test cases for Purchase Home, My Submissions, Pending Requests, Previous Requests pages."""

    def setUp(self):
        """Setup objects required across test cases."""
        self.address = Address.objects.create(address='QrNo 7/B, Street - 1, Sector 8', town_city='Bhilai',
                                              district='Durg', state='Chhattisgarh', country='India', zipcode=490009)
        self.department = Department.objects.create(name='Computer Science and Engineering', short_name='CSE',
                                                    description='Computer Science')
        self.pay = Pay.objects.create(band=18000, grade=12000, da=24000, hra=12000, ta=6000, nps=2000, lic=2000)

        # Define test normal user
        self.user = User.objects.create_user('normalemployee', 'jainendra.mandavi@iitrpr.ac.in', 'qweasdzxc',
                                             first_name='Jainendra', last_name='Mandavi')

        # Define test Accounts Department user
        self.user_accounts = User.objects.create_user('accounts_employee', 'jitin@iitrpr.ac.in', 'qweasdzxc',
                                                      first_name='Jitin', last_name='Madhu')

        self.group_accounts = Group.objects.create(name='AccountsDepartment')
        self.group_accounts.user_set.add(self.user_accounts)

        # Define test Purchase Department user
        self.user_purchase = User.objects.create_user('purchase_employee', 'basil@iitrpr.ac.in', 'qweasdzxc',
                                                      first_name='Basil', last_name='Varghese')

        self.group_purchase = Group.objects.create(name='PurchaseDepartment')
        self.group_purchase.user_set.add(self.user_purchase)

    def test_purchase_all_approved_as_employee(self):
        """Test if purchase index (home) view is being rendered without errors."""
        self.client.post(reverse('home:login'), {'username': 'normalemployee', 'password': 'qweasdzxc'})
        response = self.client.get(reverse('purchase:purchase-index'))
        self.assertNotContains(response, 'All Approved Requests', status_code=200)

        response = self.client.get(reverse('purchase:purchase-requests-approved'))
        self.assertEqual(response.status_code, 403)

    def test_purchase_all_approved_as_purchase_user(self):
        """Test if purchase index (home) view is being rendered without errors."""
        self.client.post(reverse('home:login'), {'username': 'purchase_employee', 'password': 'qweasdzxc'})
        response = self.client.get(reverse('purchase:purchase-index'))
        self.assertContains(response, 'All Approved Requests', status_code=200)

        response = self.client.get(reverse('purchase:purchase-requests-approved'))
        self.assertEqual(response.status_code, 200)

    def test_purchase_all_approved_as_accounts_user(self):
        """Test if purchase index (home) view is being rendered without errors."""
        self.client.post(reverse('home:login'), {'username': 'purchase_employee', 'password': 'qweasdzxc'})
        response = self.client.get(reverse('purchase:purchase-index'))
        self.assertContains(response, 'All Approved Requests', status_code=200)

        response = self.client.get(reverse('purchase:purchase-requests-approved'))
        self.assertEqual(response.status_code, 200)
