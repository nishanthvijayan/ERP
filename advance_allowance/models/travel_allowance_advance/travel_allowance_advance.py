from django.db import models
from django_fsm import FSMField,transition
from erp_core.models import BaseModel
from django.forms import forms


from erp_core.models.employee import Employee
from erp import settings
from state import STATE


class TravelAllowanceAdvance(BaseModel):
    """
    This stores all the information regarding travel allowance advance form and all the attachments(bills/letters).
    """
    employee = models.ForeignKey(
        Employee,
        help_text='Employee Detail'
    )
    visit_purpose= models.CharField(
        max_length=100,
        help_text='Briefly describe the visit'
    )
    budget_head= models.CharField(
        max_length=100,
        help_text='Mention the budget head, for ex. Project/Institute/Any Other'
    )
    project_name = models.CharField(
        max_length=100,
        help_text='Mention the project name'
    )
    project_no = models.IntegerField(
        help_text='Mention the project number'
    )
    advance_amount_required = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text='Enter the amount required in advance'
    )
    bus_train_air_fare = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text='Enter the fare amount as mentioned in the attached bill'
    )
    taxi_fare = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text='Enter the taxi fare amount, if any'
    )
    food_expenses = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text='Enter the food expenses'
    )
    accomodation_charges = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text='Enter the accommodation/hotel charges'
    )
    registration_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text='Enter the registration fee as mentioned in attachment'
    )
    total_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text='Total reimbursed amount'
    )
    funds_available = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text='Amount of funds available under this budget head'
    )
    amount_passed = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text='Mention the amount sanctioned'
    )
    letter=models.ImageField(
        null=False,
        blank=False,
        help_text='Attach image of the recommendation or invitation letter'
    )
    fare=models.ImageField(
        null=False,
        blank=False,
        help_text='Attach image of bus/air/train ticket'
    )
    registration_image=models.ImageField(
        help_text='Attach image of registration fee'
    )
    state=FSMField(
        null=True,
        blank=True,
        protected=not settings.DEBUG,
        default=STATE.SUBMITTED,
    )

    @transition(field=state, source=STATE.SUBMITTED, target=STATE.APPROVED_BY_HOD)
    def approve_by_hod(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_HOD, target=STATE.APPROVED_BY_JRA)
    def approve_by_jra(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_JRA, target=STATE.APPROVED_BY_ARA)
    def approve_by_ara(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_ARA, target=STATE.APPROVED_BY_R)
    def approve_by_r(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.SUBMITTED, target=STATE.REJECTED_BY_HOD)
    def rejected_by_hod(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_HOD, target=STATE.REJECTED_BY_JRA)
    def rejected_by_jra(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_JRA, target=STATE.REJECTED_BY_ARA)
    def rejected_by_ara(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    @transition(field=state, source=STATE.APPROVED_BY_ARA, target=STATE.REJECTED_BY_R)
    def rejected_by_r(self):
        """
        Transition function for django-fsm which changes the state of the model upon call
        Look into the django-fsm documentation for more
        This function may contain side-effects,
        like updating caches, notifying users, etc.
        :return: null
        """
        pass

    def clean(self):
        """
        This method overrides the default clean method of BaseModel.Model.
        This function add extra functionality that checks
         > if at least one claim amount is mentioned
        :return:
        """
        if self.registration_fee:
            if not self.registration_image:
                raise forms.ValidationError('Please upload registration image')

        if self.bus_train_air_fare:
            if not self.fare:
                raise forms.ValidationError('Please upload fare ticket image')

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)
