from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.forms import modelformset_factory

from erp_core.models.address import Address
from erp_core.models.department import Department
from erp_core.models.employee import Employee
from erp_core.models.pay import Pay

from reimbursement.models.telephone_expense.bill.bill_detail import BillDetail
from reimbursement.models.telephone_expense.bill.bill_image import BillImage

from reimbursement.forms.telephone_expense.bill.bill_detail import BillDetailForm
from reimbursement.forms.telephone_expense.bill.bill_image import BillImageForm


class NewTelephoneReimbursementViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'jainendramandavi', 'jainendra.mandavi@iitrpr.ac.in',
            'qweasdzxc', first_name='Jainendra', last_name='Mandavi'
        )
        self.address = Address.objects.create(
            address='QrNo 7/B, Street - 1, Sector 8',
            town_city='Bhilai', district='Durg',
            state='Chhattisgarh', country='India', zipcode=490009
        )
        self.department = Department.objects.create(
            name='Computer Science and Engineering', short_name='CSE',

            description='Computer Waale Noobde'
        )
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
        self.client.post(reverse('home:login'), {'username': 'jainendramandavi', 'password': 'qweasdzxc'})

    def test_new_view(self):
        data = {
            'SUBMITTED': 'Submit',

            'bill-detail-formset-MIN_NUM_FORMS': '0',
            'bill-detail-formset-MAX_NUM_FORMS': '1000',
            'bill-detail-formset-TOTAL_FORMS': '2',
            'bill-detail-formset-INITIAL_FORMS': '0',

            'bill-detail-formset-1-phone_number': '07882272628',
            'bill-detail-formset-1-bill_date': '2017-03-02',
            'bill-detail-formset-1-bill_number': '12',
            'bill-detail-formset-1-is_telephone_line': 'on',
            'bill-detail-formset-1-date_to': '2017-03-02',
            'bill-detail-formset-1-date_from': '2017-03-02',
            'bill-detail-formset-1-amount': '500',

            'bill-detail-formset-0-date_to': '2017-03-02',
            'bill-detail-formset-0-bill_number': '20',
            'bill-detail-formset-0-bill_date': '2017-03-02',
            'bill-detail-formset-0-date_from': '2017-02-03',
            'bill-detail-formset-0-phone_number': '9023632570',
            'bill-detail-formset-0-amount': '1000',


            'bill-image-formset-INITIAL_FORMS': '0',
            'bill-image-formset-MIN_NUM_FORMS': '0',
            'bill-image-formset-MAX_NUM_FORMS': '1000',
            'bill-image-formset-TOTAL_FORMS': '2',

            'bill-image-formset-0-image_file': open('../a.jpg', 'r'),
            'bill-image-formset-1-image_file': open('../b.jpg', 'r')
        }

        bill_detail_modelformset = modelformset_factory(
            BillDetail,
            form=BillDetailForm,
        )
        bill_image_modelformset = modelformset_factory(
            BillImage,
            form=BillImageForm,
        )

        bill_detail_formset = bill_detail_modelformset(
            data=data,
            prefix="bill-detail-formset",
            queryset=BillDetail.objects.none()
        )
        bill_image_formset = bill_image_modelformset(
            data,
            prefix="bill-image-formset",
            queryset=BillImage.objects.none()
        )

        self.assertTrue(bill_detail_formset.is_valid())
        self.assertTrue(bill_image_formset.is_valid())

        response = self.client.post(reverse('reimbursement:telephone-expense-new'), data)
        self.assertRedirects(
            response=response,
            expected_url=reverse('reimbursement:telephone-expense-show', kwargs={"telephone_expense_id": 1})
        )
        #
        # medical = Medical.objects.filter(general_detail__employee__user_id=self.user.id).first()
        # self.assertTrue(medical)
        #
        # bill_detail = [
        #     ['bill-detail-formset-1-phone_number', '07882272628'],
        #     ['bill-detail-formset-0-date_to', '2017-03-02'],
        #     ['bill-detail-formset-INITIAL_FORMS', '0'],
        #     ['bill-detail-formset-1-bill_date', '2017-03-02'],
        #     ['bill-detail-formset-MIN_NUM_FORMS', '0'],
        #     ['bill-detail-formset-1-date_from', '2017-03-02'],
        #     ['bill-detail-formset-0-phone_number', '9023632570'],
        #     ['bill-detail-formset-1-amount', '500'],
        #     ['bill-detail-formset-MAX_NUM_FORMS', '1000'],
        #     ['bill-detail-formset-TOTAL_FORMS', '2'],
        #     ['bill-detail-formset-0-amount', '1000'],
        #     ['bill-detail-formset-1-bill_number', '12'],
        #     ['bill-detail-formset-0-bill_number', '20'],
        #     ['bill-detail-formset-1-is_telephone_line', 'on'],
        #     ['bill-detail-formset-0-bill_date', '2017-03-02'],
        #     ['bill-detail-formset-0-date_from', '2017-02-03'],
        #     ['bill-detail-formset-1-date_to', '2017-03-02'],
        # ]
        # bill_image = [
        #     ['bill-image-formset-INITIAL_FORMS', '0'],
        #     ['bill-image-formset-MIN_NUM_FORMS', '0'],
        #     ['bill-image-formset-0-image_file', '']
        #     ['bill-image-formset-MAX_NUM_FORMS', '1000'],
        #     ['bill-image-formset-TOTAL_FORMS', '1'],
        # ]
        #
        # general_detail = [
        #     [medical.general_detail.patient_name, 'Jainendra Mandavi'],
        #     [medical.general_detail.patient_age, '23'],
        #     [medical.general_detail.employee_relationship, 'Self'],
        # ]
        # medical_detail = [
        #     [medical.medical_detail.specialist_consultant_hospital, ''],
        #     [medical.medical_detail.consultation_place, 'Bhilai'],
        #     [medical.medical_detail.cost_of_medicines_market, ''],
        #     [medical.medical_detail.less_advance_taken, '0'],
        #     [medical.medical_detail.total_amount_claimed, '1400'],
        #     [medical.medical_detail.consultant_designation, 'Head Physician'],
        #     [medical.medical_detail.place_at_which_patient_fell_ill, 'Bhilai'],
        #     [medical.medical_detail.injection_place, 'Bhilai'],
        #     [medical.medical_detail.specialist_consultant_designation, ''],
        #     [medical.medical_detail.diagnosis_place, 'Bhilai'],
        #     [medical.medical_detail.diagnosis_advised_certificate, ''],
        #     [medical.medical_detail.consultant_name, 'Dr. Batra'],
        #     [medical.medical_detail.consultant_hospital, 'JLNH'],
        #     [medical.medical_detail.net_amount_taken, '1400'],
        #     [medical.medical_detail.specialist_consultant_name, ''],
        # ]
        # consultation_detail = [
        #     [medical.medical_detail.consultation.all()[0].date, '2017-05-02'],
        #     [medical.medical_detail.consultation.all()[0].fee, '200']
        # ]
        # injection_detail = [
        #     [medical.medical_detail.injection.all()[0].date, '2017-05-02'],
        #     [medical.medical_detail.injection.all()[0].fee, '200']
        # ]
        # specialist_consultation_detail = [
        #     ['specialist_consultation_formset-MAX_NUM_FORMS', '1000'],
        #     ['specialist_consultation_formset-TOTAL_FORMS', '1'],
        #     ['specialist_consultation_formset-0-fee', ''],
        #     ['specialist_consultation_formset-INITIAL_FORMS', '0'],
        #     ['specialist_consultation_formset-0-date', ''],
        #     ['specialist_consultation_formset-MIN_NUM_FORMS', '0']
        # ]
        #
        # def xstr(s):
        #     if s is None:
        #         return ''
        #     return str(s).replace('.00','')
        #
        # for gd in general_detail:
        #     self.assertEqual(xstr(gd[0]), gd[1])
        #
        # for md in medical_detail:
        #     self.assertEqual(xstr(md[0]), md[1])
        #
        # for c in consultation_detail:
        #     self.assertEqual(xstr(c[0]),c[1])
        #
        # for i in injection_detail:
        #     self.assertEqual(xstr(i[0]),i[1])
        #
        # # for sc in specialist_consultation_detail:
        # #     self.assertEqual(xstr(sc[0]),sc[1])
        # self.assertEqual(len(medical.medical_detail.specialist_consultation.all()), 2)
