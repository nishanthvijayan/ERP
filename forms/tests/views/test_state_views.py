from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from forms.models import State, Workflow


class StateViewTests(TestCase):
    def setUp(self):
        self.workflow = Workflow.objects.create(name="Example Workflow", description="This is a test workflow")
        self.state = State.objects.create(workflow=self.workflow, name="Example State", kind="Initial")
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.post(reverse('home:login'), {'username': 'john', 'password': 'johnpassword'})

    def test_new_view(self):
        state_count_before = State.objects.count()
        response = self.client.get(reverse('forms:state-new', kwargs={"workflow_id": self.workflow.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('forms:state-new', kwargs={"workflow_id": self.workflow.id}), {'name': 'New State', 'kind': 'Accepted'})
        self.assertRedirects(response, reverse('forms:workflow-show', kwargs={"workflow_id": self.workflow.id}))
        self.assertEqual(State.objects.count(), state_count_before + 1)

    def test_edit_view(self):
        response = self.client.get(reverse('forms:state-edit', kwargs={"workflow_id": self.workflow.id, "state_id": self.state.id}))
        self.assertEqual(response.status_code, 200)

        new_data = {'name': 'Updated State Name', 'kind': 'Initial'}
        response = self.client.post(reverse('forms:state-edit', kwargs={"workflow_id": self.workflow.id, "state_id": self.state.id}), new_data)
        self.assertRedirects(response, reverse('forms:workflow-show', kwargs={"workflow_id": self.workflow.id}))
        updated_state = State.objects.get(pk=self.state.id)
        self.assertEqual(updated_state.name, 'Updated State Name')

    def test_delete_view(self):
        state_count_before = State.objects.count()
        response = self.client.get(reverse('forms:state-delete', kwargs={"workflow_id": self.workflow.id, "state_id": self.state.id}))
        self.assertRedirects(response, reverse('forms:workflow-show', kwargs={"workflow_id": self.workflow.id}))
        self.assertEqual(State.objects.count(), state_count_before - 1)
