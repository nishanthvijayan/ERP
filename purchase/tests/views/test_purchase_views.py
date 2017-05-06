"""Test cases for Purchase Home, My Submissions, Pending Requests, Previous Requests pages."""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

from purchase.models import PurchaseIndentRequest
from erp_core.models import Employee, Address, Department, Pay


class PurchaseViewTests(TestCase):
    """Test cases for Purchase Home, My Submissions, Pending Requests, Previous Requests pages."""

    def setUp(self):
        """Setup objects required across test cases."""
        self.address = Address.objects.create(address='QrNo 7/B, Street - 1, Sector 8', town_city='Bhilai',
                                              district='Durg', state='Chhattisgarh', country='India', zipcode=490009)
        self.department = Department.objects.create(name='Computer Science and Engineering', short_name='CSE',
                                                    description='Computer Science')
        self.pay = Pay.objects.create(band=18000, grade=12000, da=24000, hra=12000, ta=6000, nps=2000, lic=2000)

        # Define test indenter user
        self.user = User.objects.create_user('jainendramandavi', 'jainendra.mandavi@iitrpr.ac.in', 'qweasdzxc',
                                             first_name='Jainendra', last_name='Mandavi')
        self.employee = Employee.objects.create(
            employee_id=30052, nationality='Indian', date_of_joining='2017-04-21',
            designation='Head of Department', short_designation='HOD', user=self.user, department=self.department,
            current_address=self.address, permanent_address=self.address, pay=self.pay
        )

        # Define test HOD user
        self.user_hod = User.objects.create_user('nishanthvijayan', 'nishanth.vijayan@iitrpr.ac.in', 'qweasdzxc',
                                                 first_name='Nishanth', last_name='Vijayan')
        self.employee_hod = Employee.objects.create(
            employee_id=30056, nationality='Indian', date_of_joining='2017-04-21',
            designation='Assistant Accounting Officer', short_designation='A+1AO', user=self.user_hod,
            department=self.department, current_address=self.address,
            permanent_address=self.address, pay=self.pay
        )
        self.department.head = self.employee_hod
        self.department.save()

        # Define JAO user
        self.user_jao = User.objects.create_user('jitin', 'jitin@iitrpr.ac.in', 'qweasdzxc',
                                                 first_name='Jitin', last_name='Madhu')
        self.employee_jao = Employee.objects.create(
            employee_id=33046, nationality='Indian', date_of_joining='2017-04-21',
            designation='Junior Accounts Officer', short_designation='JAO', user=self.user_jao,
            department=self.department, current_address=self.address,
            permanent_address=self.address, pay=self.pay
        )
        self.group_jao = Group.objects.create(name='JAO_AccountsDepartment')
        self.group_jao.user_set.add(self.user_jao)

        # Define test DR user
        self.user_dr = User.objects.create_user('basil', 'basil@iitrpr.ac.in', 'qweasdzxc',
                                                first_name='Basil', last_name='Varghese')
        self.employee_dr = Employee.objects.create(
            employee_id=30056, nationality='Indian', date_of_joining='2017-04-21',
            designation='Deputy Registrar', short_designation='A+1AO', user=self.user_dr,
            department=self.department, current_address=self.address,
            permanent_address=self.address, pay=self.pay
        )
        self.group_dr = Group.objects.create(name='DR_AccountsDepartment')
        self.group_dr.user_set.add(self.user_dr)

    def test_purchase_index_view(self):
        """Test if purchase index (home) view is being rendered without errors."""
        self.client.post(reverse('home:login'), {'username': 'jainendramandavi', 'password': 'qweasdzxc'})
        response = self.client.get(reverse('purchase:purchase-index'))
        self.assertEqual(response.status_code, 200)

    def test_submissions_view(self):
        """Test if My Submissions page lists current users submission & only his submissions."""
        self.client.post(reverse('home:login'), {'username': 'jainendramandavi', 'password': 'qweasdzxc'})
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Mine", budget_head="Institute")
        PurchaseIndentRequest.objects.create(indenter=self.employee_hod, project_name="Not Mine",
                                             budget_head="Institute")
        response = self.client.get(reverse('purchase:purchase-submissions'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['submissions']), 1)
        self.assertEqual(response.context['submissions'][0].project_name, 'Mine')
        self.assertEqual(response.context['submissions'][0].state, 'Submitted')

    def test_pending_requests_view_employee(self):
        """Test if Pending page lists no forms regular employee."""
        self.client.post(reverse('home:login'), {'username': 'jainendramandavi', 'password': 'qweasdzxc'})
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Test hod",
                                             budget_head="Institute", state="Submitted")
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Test jr",
                                             budget_head="Institute", state="Approved by Head of Department")
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Test dr",
                                             budget_head="Institute", state="Approved by Junior Accounts Officer")
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Test reject",
                                             budget_head="Institute", state="Rejected")

        response = self.client.get(reverse('purchase:purchase-requests-pending'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['pending_requests']), 0)

    def test_pending_requests_view_hod(self):
        """Test if Pending page lists fomrs approvable by current user(hod) & only those."""
        self.client.post(reverse('home:login'), {'username': 'nishanthvijayan', 'password': 'qweasdzxc'})
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Test hod",
                                             budget_head="Institute", state="Submitted")
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Test jr",
                                             budget_head="Institute", state="Approved by Head of Department")
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Test dr",
                                             budget_head="Institute", state="Approved by Junior Accounts Officer")
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Test reject",
                                             budget_head="Institute", state="Rejected")

        response = self.client.get(reverse('purchase:purchase-requests-pending'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['pending_requests']), 1)
        self.assertEqual(response.context['pending_requests'][0].project_name, 'Test hod')

    def test_pending_requests_view_jao(self):
        """Test if Pending page lists fomrs approvable by current user(jao) & only those."""
        response = self.client.post(reverse('home:login'), {'username': 'jitin', 'password': 'qweasdzxc'})
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Test hod",
                                             budget_head="Institute", state="Submitted")
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Test jao",
                                             budget_head="Institute", state="Approved by Head of Department")
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Test dr",
                                             budget_head="Institute", state="Approved by Junior Accounts Officer")
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Test reject",
                                             budget_head="Institute", state="Rejected")

        response = self.client.get(reverse('purchase:purchase-requests-pending'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['pending_requests']), 1)
        self.assertEqual(response.context['pending_requests'][0].project_name, 'Test jao')

    def test_pending_requests_view_dr(self):
        """Test if Pending page lists forms approvable by current user (dr) & only those."""
        response = self.client.post(reverse('home:login'), {'username': 'basil', 'password': 'qweasdzxc'})
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Test hod",
                                             budget_head="Institute", state="Submitted")
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Test jr",
                                             budget_head="Institute", state="Approved by Head of Department")
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Test dr",
                                             budget_head="Institute", state="Approved by Junior Accounts Officer")
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Test reject",
                                             budget_head="Institute", state="Rejected")
        response = self.client.get(reverse('purchase:purchase-requests-pending'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['pending_requests']), 1)
        self.assertEqual(response.context['pending_requests'][0].project_name, 'Test dr')

    def test_previous_requests_view_employee(self):
        """Test if Previous Requests page lists no forms for a regular employee."""
        response = self.client.post(reverse('home:login'), {'username': 'jainendramandavi', 'password': 'qweasdzxc'})
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Test hod",
                                             budget_head="Institute", state="Submitted")
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Test jr",
                                             budget_head="Institute", state="Approved by Head of Department")
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Test dr",
                                             budget_head="Institute", state="Approved by Junior Accounts Officer")
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Test reject",
                                             budget_head="Institute", state="Rejected")
        response = self.client.get(reverse('purchase:purchase-requests-previous'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['previous_requests']), 0)

    def test_previous_requests_view_hod(self):
        """Test if Previous Requests page lists forms appropriately for HOD."""
        response = self.client.post(reverse('home:login'), {'username': 'nishanthvijayan', 'password': 'qweasdzxc'})
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Project_one",
                                             budget_head="Institute", state="Submitted")
        second_form = PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Project_two",
                                                           budget_head="Institute", state="Submitted")
        third_form = PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Project_three",
                                                          budget_head="Institute", state="Submitted")

        """Three forms are 3 in a state that can be accpted by the current user who is the HOD
        of the indenter of the 3 forms. So on visiting Pending Requests page initially it should
        display 3 forms.Since no forms have been approved previously Previous Requests page should
        not display any item"""
        response = self.client.get(reverse('purchase:purchase-requests-pending'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['pending_requests']), 3)
        response = self.client.get(reverse('purchase:purchase-requests-previous'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['previous_requests']), 0)

        """We simulate accpeting a form. Now there should be 2 pending forms and 1 forms in
        Previous Requests."""
        self.client.post(reverse('purchase:purchase-indent-hod-approve',
                                 kwargs={"request_id": second_form.id}), {'Approve': 'Approve', 'remark': ''})
        response = self.client.get(reverse('purchase:purchase-requests-pending'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['pending_requests']), 2)

        response = self.client.get(reverse('purchase:purchase-requests-previous'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['previous_requests']), 1)

        """We simulate rejecting a form. Now there should be 1 pending form and 2 forms in
        Previous Requests page"""
        self.client.post(reverse('purchase:purchase-indent-hod-approve',
                                 kwargs={"request_id": third_form.id}), {'Reject': 'Reject', 'remark': ''})
        response = self.client.get(reverse('purchase:purchase-requests-pending'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['pending_requests']), 1)

        response = self.client.get(reverse('purchase:purchase-requests-previous'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['previous_requests']), 2)

    def test_previous_requests_view_jao(self):
        """Test if Previous Requests page lists forms appropriately for JAO."""
        response = self.client.post(reverse('home:login'), {'username': 'jitin', 'password': 'qweasdzxc'})
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Project_one",
                                             budget_head="Institute", state="Approved by Head of Department")
        second_form = PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Project_two",
                                                           budget_head="Institute",
                                                           state="Approved by Head of Department")
        third_form = PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Project_three",
                                                          budget_head="Institute",
                                                          state="Approved by Head of Department")

        """Three forms are 3 in a state that can be accpted by the current user who is the JAO.
        So on visiting Pending Requests page initially it should display 3 forms.
        Since no forms have been approved previously Previous Requests page should not display any item"""
        response = self.client.get(reverse('purchase:purchase-requests-pending'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['pending_requests']), 3)
        response = self.client.get(reverse('purchase:purchase-requests-previous'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['previous_requests']), 0)

        """We simulate accpeting a form. Now there should be 2 pending forms and 1 forms in
        Previous Requests."""
        self.client.post(reverse('purchase:purchase-indent-jao-approve', kwargs={"request_id": second_form.id}),
                         {'Approve': 'Approve', 'remark': '',
                          'budget_sanctioned': 1000.34, 'amount_already_spent': 34.5, 'budget_available': 45.24})
        response = self.client.get(reverse('purchase:purchase-requests-pending'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['pending_requests']), 2)

        response = self.client.get(reverse('purchase:purchase-requests-previous'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['previous_requests']), 1)

        """We simulate rejecting a form. Now there should be 1 pending form and 2 forms in
        Previous Requests page"""
        self.client.post(reverse('purchase:purchase-indent-jao-approve', kwargs={"request_id": third_form.id}),
                         {'Reject': 'Reject', 'remark': '',
                          'budget_sanctioned': 1000.34, 'amount_already_spent': 34.5, 'budget_available': 45.24})
        response = self.client.get(reverse('purchase:purchase-requests-pending'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['pending_requests']), 1)

        response = self.client.get(reverse('purchase:purchase-requests-previous'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['previous_requests']), 2)

    def test_previous_requests_view_dr(self):
        """Test if Previous Requests page lists forms appropriately for DR."""
        response = self.client.post(reverse('home:login'), {'username': 'basil', 'password': 'qweasdzxc'})
        PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Project_one",
                                             budget_head="Institute", state="Approved by Junior Accounts Officer")
        second_form = PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Project_two",
                                                           budget_head="Institute",
                                                           state="Approved by Junior Accounts Officer")
        third_form = PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Project_three",
                                                          budget_head="Institute",
                                                          state="Approved by Junior Accounts Officer")

        """Three forms are 3 in a state that can be accpted by the current user who is the DR.
        So on visiting Pending Requests page initially it should display 3 forms.
        Since no forms have been approved previously Previous Requests page should not display any item"""
        response = self.client.get(reverse('purchase:purchase-requests-pending'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['pending_requests']), 3)
        response = self.client.get(reverse('purchase:purchase-requests-previous'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['previous_requests']), 0)

        """We simulate accpeting a form. Now there should be 2 pending forms and 1 forms in
        Previous Requests."""
        self.client.post(reverse('purchase:purchase-indent-dr-approve',
                                 kwargs={"request_id": second_form.id}), {'Approve': 'Approve', 'remark': ''})
        response = self.client.get(reverse('purchase:purchase-requests-pending'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['pending_requests']), 2)

        response = self.client.get(reverse('purchase:purchase-requests-previous'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['previous_requests']), 1)

        """We simulate rejecting a form. Now there should be 1 pending form and 2 forms in
        Previous Requests page"""
        self.client.post(reverse('purchase:purchase-indent-dr-approve',
                                 kwargs={"request_id": third_form.id}), {'Reject': 'Reject', 'remark': ''})
        response = self.client.get(reverse('purchase:purchase-requests-pending'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['pending_requests']), 1)

        response = self.client.get(reverse('purchase:purchase-requests-previous'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['previous_requests']), 2)
