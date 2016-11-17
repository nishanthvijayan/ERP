from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from forms.models import FormElement, Workflow

class FormElementViewTests(TestCase):
    def setUp(self):
        self.workflow = Workflow.objects.create(name="Example Workflow", description="This is a test workflow")
        self.form_element = FormElement.objects.create(workflow=self.workflow, caption="Name", hint="This is just a dummy field", position=1, element_type="text_input")
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.post(reverse('home:login'), {'username': 'john', 'password': 'johnpassword'})

    def test_new_view(self):
        form_element_count_before = FormElement.objects.count()
        response = self.client.get(reverse('forms:form-element-new', kwargs={"workflow_id": self.workflow.id}))
        self.assertEqual(response.status_code, 200)

        data = {'caption': 'Occupation', 'hint': 'This is just a test', "position": 1, "element_type": "text_input"}
        response = self.client.post(reverse('forms:form-element-new', kwargs={"workflow_id": self.workflow.id}), data)
        self.assertRedirects(response, reverse('forms:workflow-show', kwargs={"workflow_id": self.workflow.id}))
        self.assertEqual(FormElement.objects.count(), form_element_count_before + 1)

    def test_edit_view(self):
        response = self.client.get(reverse('forms:form-element-edit', kwargs={"workflow_id": self.workflow.id, "element_id": self.form_element.id}))
        self.assertEqual(response.status_code, 200)

        new_data = {'caption': 'Occupation', 'hint': 'This is just a test', "position": 1, "element_type": "text_input"}
        response = self.client.post(reverse('forms:form-element-edit', kwargs={"workflow_id": self.workflow.id, "element_id": self.form_element.id}), new_data)
        self.assertRedirects(response, reverse('forms:workflow-show', kwargs={"workflow_id": self.workflow.id}))
        updated_form_element = FormElement.objects.get(pk=self.form_element.id)
        self.assertEqual(updated_form_element.caption, 'Occupation')

    def test_delete_view(self):
        form_element_count_before = FormElement.objects.count()
        response = self.client.get(reverse('forms:form-element-delete', kwargs={"workflow_id": self.workflow.id, "element_id": self.form_element.id}))
        self.assertRedirects(response, reverse('forms:workflow-show', kwargs={"workflow_id": self.workflow.id}))
        self.assertEqual(FormElement.objects.count(), form_element_count_before - 1)
