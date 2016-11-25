from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from forms.models import Workflow


class WorkflowViewTests(TestCase):
    def setUp(self):
        self.workflow = Workflow.objects.create(name="Leave Application", description="Testing a Leave Application")
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.post(reverse('home:login'), {'username': 'john', 'password': 'johnpassword'})

    def test_index_view(self):
        response = self.client.get(reverse('forms:workflow-index'))
        self.assertEqual(response.status_code, 200)

    def test_show_view(self):
        response = self.client.get(reverse('forms:workflow-show', kwargs={"workflow_id": self.workflow.id}))
        self.assertEqual(response.status_code, 200)

    def test_new_view(self):
        response = self.client.get(reverse('forms:workflow-new'))
        self.assertEqual(response.status_code, 200)

        workflow_count_before = Workflow.objects.count()
        response = self.client.post(reverse('forms:workflow-new'), {'name': 'New Workflow', 'description': 'Test Workflow Description'})
        self.assertRedirects(response, reverse('forms:workflow-index'))
        self.assertEqual(Workflow.objects.count(), workflow_count_before + 1)

    def test_edit_view(self):
        response = self.client.get(reverse('forms:workflow-edit', kwargs={"workflow_id": self.workflow.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('forms:workflow-edit', kwargs={"workflow_id": self.workflow.id}), {'name': 'Leave Workflow', 'description': 'Updated Workflow'})
        self.assertRedirects(response, reverse('forms:workflow-index'))
        updated_workflow = Workflow.objects.get(pk=self.workflow.id)
        self.assertEqual(updated_workflow.description, 'Updated Workflow')

    def test_delete_view(self):
        workflow_count_before = Workflow.objects.count()
        response = self.client.get(reverse('forms:workflow-delete', kwargs={"workflow_id": self.workflow.id}))
        self.assertRedirects(response, reverse('forms:workflow-index'))
        self.assertEqual(Workflow.objects.count(), workflow_count_before - 1)
