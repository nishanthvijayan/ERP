from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

from erp_core.models.address import Address
from erp_core.models.department import Department
from erp_core.models.employee import Employee
from erp_core.models.pay import Pay

from models.medical.medical import Medical
from forms.medical.general_detail.general_detail import GeneralDetailForm
from forms.medical.medical_detail.medical_detail import MedicalDetailForm


class NewMedicalReimbursementViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('jainendramandavi', 'jainendra.mandavi@iitrpr.ac.in', 'qweasdzxc',
                                        first_name='Jainendra', last_name='Mandavi')
        self.address = Address.objects.create(address='QrNo 7/B, Street - 1, Sector 8', town_city='Bhilai', district='Durg',
                                         state='Chhattisgarh', country='India', zipcode=490009)
        self.department = Department.objects.create(name='Computer Science and Engineering', short_name='CSE',
                                               description='Computer Waale Noobde')
        self.pay = Pay.objects.create(band=18000, grade=12000, da=24000, hra=12000, ta=6000, nps=2000, lic=2000)
        self.employee = Employee.objects.create(
                                            employee_id=30052, nationality='Indian',
                                            date_of_joining='2017-04-21',
                                            designation='Head of Department',
                                            short_designation='HOD',
                                            user=self.user,
                                            department=self.department,
                                            current_address=self.address,
                                            permanent_address=self.address,
                                            pay=self.pay
                                        )
        self.group = Group.objects.create(name='Employee')
        self.group.user_set.add(self.user)
        # self.user = User.objects.create_user('gurpreetsingh', 'gurpreet.singh@iitrpr.ac.in', 'qweasdzxc',
        #                                 first_name='gurpreet', last_name='Singh')
        # self.address = Address.objects.create(address='Block No 4/A, Street - 1, Sector 14', town_city='Chandigarh',
        #                                  district='Chandigarh', state='Chandigarh', country='India', zipcode=170009)
        # self.department = Department.objects.create(name='Accounts Department', short_name='AD',
        #                                        description='Manages Accounts')
        # self.pay = Pay.objects.create(band=15000, grade=8000, da=24000, hra=12000, ta=6000, nps=2000, lic=2000)
        # self.employee = Employee.objects.create(
        #                                     employee_id=30056,
        #                                     nationality='Indian',
        #                                     date_of_joining='2017-04-21',
        #                                     designation='Assistant Accounting Officer',
        #                                     short_designation='A+1AO',
        #                                     user=self.user,
        #                                     department=self.department,
        #                                     current_address=self.address,
        #                                     permanent_address=self.address,
        #                                     pay=self.pay
        # )
        self.client.post(reverse('home:login'), {'username': 'jainendramandavi', 'password': 'qweasdzxc'})

    def test_new_view(self):
        data = {
            'general_detail_form-patient_name': 'Jainendra Mandavi',
            'general_detail_form-patient_age': '23',
            'general_detail_form-employee_relationship': 'Self',

            'medical_detail_form-specialist_consultant_hospital': '',
            'medical_detail_form-consultation_place': 'Bhilai',
            'medical_detail_form-cost_of_medicines_market': '',
            'medical_detail_form-less_advance_taken': '0',
            'medical_detail_form-total_amount_claimed': '1400',
            'medical_detail_form-consultant_designation': 'Head Physician',
            'medical_detail_form-place_at_which_patient_fell_ill': 'Bhilai',
            'medical_detail_form-injection_place': 'Bhilai',
            'medical_detail_form-specialist_consultant_designation': '',
            'medical_detail_form-diagnosis_place': 'Bhilai',
            'medical_detail_form-diagnosis_advised_certificate': '',
            'medical_detail_form-consultant_name': 'Dr. Batra',
            'medical_detail_form-consultant_hospital': 'JLNH',
            'medical_detail_form-net_amount_taken': '1400',
            'medical_detail_form-specialist_consultant_name': '',
            'SUBMITTED': 'Submit',

            'consultation_formset-INITIAL_FORMS': '0',
            'consultation_formset-MAX_NUM_FORMS': '1000',
            'consultation_formset-0-date': '2017-05-02',
            'consultation_formset-MIN_NUM_FORMS': '0',
            'consultation_formset-TOTAL_FORMS': '1',
            'consultation_formset-0-fee': '200',

            'injection_formset-MAX_NUM_FORMS': '1000',
            'injection_formset-0-date': '2017-05-02',
            'injection_formset-TOTAL_FORMS': '1',
            'injection_formset-INITIAL_FORMS': '0',
            'injection_formset-0-fee': '200',
            'injection_formset-MIN_NUM_FORMS': '0',

            'specialist_consultation_formset-MAX_NUM_FORMS': '1000',
            'specialist_consultation_formset-TOTAL_FORMS': '1',
            'specialist_consultation_formset-0-fee': '',
            'specialist_consultation_formset-INITIAL_FORMS': '0',
            'specialist_consultation_formset-0-date': '',
            'specialist_consultation_formset-MIN_NUM_FORMS': '0'
        }
        self.assertTrue(GeneralDetailForm(data=data, prefix="general_detail_form").is_valid())
        self.assertTrue(MedicalDetailForm(data=data, prefix="medical_detail_form").is_valid())

        response = self.client.post(reverse('reimbursement:medical-new'), data)
        self.assertRedirects(
            response=response,
            expected_url=reverse('reimbursement:medical-show',kwargs={"medical_id": 1})
        )

        medical = Medical.objects.filter(general_detail__employee__user_id=self.user.id).first()
        self.assertTrue(medical)

        general_detail = [
            [medical.general_detail.patient_name, 'Jainendra Mandavi'],
            [medical.general_detail.patient_age, '23'],
            [medical.general_detail.employee_relationship, 'Self'],
        ]
        medical_detail = [
            [medical.medical_detail.specialist_consultant_hospital, ''],
            [medical.medical_detail.consultation_place, 'Bhilai'],
            [medical.medical_detail.cost_of_medicines_market, ''],
            [medical.medical_detail.less_advance_taken, '0'],
            [medical.medical_detail.total_amount_claimed, '1400'],
            [medical.medical_detail.consultant_designation, 'Head Physician'],
            [medical.medical_detail.place_at_which_patient_fell_ill, 'Bhilai'],
            [medical.medical_detail.injection_place, 'Bhilai'],
            [medical.medical_detail.specialist_consultant_designation, ''],
            [medical.medical_detail.diagnosis_place, 'Bhilai'],
            [medical.medical_detail.diagnosis_advised_certificate, ''],
            [medical.medical_detail.consultant_name, 'Dr. Batra'],
            [medical.medical_detail.consultant_hospital, 'JLNH'],
            [medical.medical_detail.net_amount_taken, '1400'],
            [medical.medical_detail.specialist_consultant_name, ''],
        ]
        consultation_detail = [
            [medical.medical_detail.consultation.all()[0].date, '2017-05-02'],
            [medical.medical_detail.consultation.all()[0].fee, '200']
        ]
        injection_detail = [
            [medical.medical_detail.injection.all()[0].date, '2017-05-02'],
            [medical.medical_detail.injection.all()[0].fee, '200']
        ]
        specialist_consultation_detail = [
            ['specialist_consultation_formset-MAX_NUM_FORMS', '1000'],
            ['specialist_consultation_formset-TOTAL_FORMS', '1'],
            ['specialist_consultation_formset-0-fee', ''],
            ['specialist_consultation_formset-INITIAL_FORMS', '0'],
            ['specialist_consultation_formset-0-date', ''],
            ['specialist_consultation_formset-MIN_NUM_FORMS', '0']
        ]

        def xstr(s):
            if s is None:
                return ''
            return str(s).replace('.00','')

        for gd in general_detail:
            self.assertEqual(xstr(gd[0]), gd[1])

        for md in medical_detail:
            self.assertEqual(xstr(md[0]), md[1])

        for c in consultation_detail:
            self.assertEqual(xstr(c[0]),c[1])

        for i in injection_detail:
            self.assertEqual(xstr(i[0]),i[1])

        # for sc in specialist_consultation_detail:
        #     self.assertEqual(xstr(sc[0]),sc[1])
        self.assertEqual(len(medical.medical_detail.specialist_consultation.all()), 0)