"""Test cases for Purchase Indent Request show pages."""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

from purchase.models import PurchaseIndentRequest
from erp_core.models import Employee, Address, Department, Pay


class PurchaseIndentShowViewTests(TestCase):
    """Test cases for Purchase Indent Request show pages."""

    def setUp(self):
        """Setup objects required across test cases."""
        self.address = Address.objects.create(address='QrNo 7/B, Street - 1, Sector 8', town_city='Bhilai',
                                              district='Durg', state='Chhattisgarh', country='India', zipcode=490009)
        self.department = Department.objects.create(name='Computer Science and Engineering', short_name='CSE',
                                                    description='Computer Science')
        self.pay = Pay.objects.create(band=18000, grade=12000, da=24000, hra=12000, ta=6000, nps=2000, lic=2000)

        # Define test indenter user
        self.user = User.objects.create_user('normalemployee', 'jainendra.mandavi@iitrpr.ac.in', 'qweasdzxc',
                                             first_name='Jainendra', last_name='Mandavi')
        self.employee = Employee.objects.create(
            employee_id=30052, nationality='Indian', date_of_joining='2017-04-21',
            designation='Head of Department', short_designation='HOD', user=self.user, department=self.department,
            current_address=self.address, permanent_address=self.address, pay=self.pay
        )

        # Define test HOD user
        self.user_hod = User.objects.create_user('hod_employee', 'nishanth.vijayan@iitrpr.ac.in', 'qweasdzxc',
                                                 first_name='Nishanth', last_name='Vijayan')
        self.employee_hod = Employee.objects.create(
            employee_id=30056, nationality='Indian', date_of_joining='2017-04-21',
            designation='Assistant Accounting Officer', short_designation='A+1AO', user=self.user_hod,
            department=self.department, current_address=self.address,
            permanent_address=self.address, pay=self.pay
        )
        self.department.hod = self.employee_hod
        self.department.save()

        # Define JAO user
        self.user_jao = User.objects.create_user('jao_employee', 'jitin@iitrpr.ac.in', 'qweasdzxc',
                                                 first_name='Jitin', last_name='Madhu')
        self.employee_jao = Employee.objects.create(
            employee_id=33046, nationality='Indian', date_of_joining='2017-04-21',
            designation='Junior Accounts Officer', short_designation='JAO', user=self.user_jao,
            department=self.department, current_address=self.address,
            permanent_address=self.address, pay=self.pay
        )
        self.group_jao = Group.objects.create(name='JrAO_AccountsDepartment')
        self.group_jao.user_set.add(self.user_jao)

        # Define test DR user
        self.user_dr = User.objects.create_user('dr_employee', 'basil@iitrpr.ac.in', 'qweasdzxc',
                                                first_name='Basil', last_name='Varghese')
        self.employee_dr = Employee.objects.create(
            employee_id=30056, nationality='Indian', date_of_joining='2017-04-21',
            designation='Deputy Registrar', short_designation='A+1AO', user=self.user_dr,
            department=self.department, current_address=self.address,
            permanent_address=self.address, pay=self.pay
        )
        self.group_dr = Group.objects.create(name='DR_AccountsDepartment')
        self.group_dr.user_set.add(self.user_dr)

    def test_purchase_indent_show_as_indenter(self):
        """Employee who submitted a form should be able to view it any state."""
        response = self.client.post(reverse('home:login'), {'username': 'normalemployee', 'password': 'qweasdzxc'})
        form = PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Project",
                                                    budget_head="Institute", state="Submitted")

        response = self.client.get(reverse('purchase:purchase-indent-show', kwargs={"request_id": form.id}))
        self.assertNotContains(response, 'Budget Details', 200)

        form.state = "Approved by Head of Department"
        form.save()
        response = self.client.get(reverse('purchase:purchase-indent-show', kwargs={"request_id": form.id}))
        self.assertNotContains(response, 'Budget Details', 200)

        form.state = "Approved by Junior Accounts Officer"
        form.save()
        response = self.client.get(reverse('purchase:purchase-indent-show', kwargs={"request_id": form.id}))
        self.assertContains(response, 'Budget Details', status_code=200)

        form.state = "Approved by Deputy Registrar"
        form.save()
        response = self.client.get(reverse('purchase:purchase-indent-show', kwargs={"request_id": form.id}))
        self.assertContains(response, 'Budget Details', status_code=200)

    def test_purchase_indent_show_as_hod_of_indenter(self):
        """HOD of Employee who submitted a form should be able to view it any state."""
        response = self.client.post(reverse('home:login'), {'username': 'hod_employee', 'password': 'qweasdzxc'})
        form = PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Project",
                                                    budget_head="Institute", state="Approved by Head of Department")

        response = self.client.get(reverse('purchase:purchase-indent-show', kwargs={"request_id": form.id}))
        self.assertNotContains(response, 'Budget Details', 200)

        form.state = "Approved by Junior Accounts Officer"
        form.save()
        response = self.client.get(reverse('purchase:purchase-indent-show', kwargs={"request_id": form.id}))
        self.assertContains(response, 'Budget Details', status_code=200)

        form.state = "Approved by Deputy Registrar"
        form.save()
        response = self.client.get(reverse('purchase:purchase-indent-show', kwargs={"request_id": form.id}))
        self.assertContains(response, 'Budget Details', status_code=200)

    def test_purchase_indent_show_as_jao(self):
        """HOD of Employee who submitted a form should be able to view it any state."""
        response = self.client.post(reverse('home:login'), {'username': 'jao_employee', 'password': 'qweasdzxc'})
        form = PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Project",
                                                    budget_head="Institute",
                                                    state="Approved by Junior Accounts Officer")

        response = self.client.get(reverse('purchase:purchase-indent-show', kwargs={"request_id": form.id}))
        self.assertContains(response, 'Budget Details', status_code=200)

        form.state = "Approved by Deputy Registrar"
        form.save()
        response = self.client.get(reverse('purchase:purchase-indent-show', kwargs={"request_id": form.id}))
        self.assertContains(response, 'Budget Details', status_code=200)

    def test_purchase_indent_show_as_dr(self):
        """HOD of Employee who submitted a form should be able to view it any state."""
        response = self.client.post(reverse('home:login'), {'username': 'dr_employee', 'password': 'qweasdzxc'})
        form = PurchaseIndentRequest.objects.create(indenter=self.employee, project_name="Project",
                                                    budget_head="Institute", state="Approved by Deputy Registrar")

        response = self.client.get(reverse('purchase:purchase-indent-show', kwargs={"request_id": form.id}))
        self.assertContains(response, 'Budget Details', status_code=200)
