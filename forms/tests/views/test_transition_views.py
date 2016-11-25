from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group, User

from forms.models import State, Workflow, Transition


class TransitionViewTests(TestCase):
    def setUp(self):
        self.workflow = Workflow.objects.create(name="Example Workflow", description="This is a test workflow")
        self.state_one = State.objects.create(workflow=self.workflow, name="Example State 1", kind="Initial")
        self.state_two = State.objects.create(workflow=self.workflow, name="Example State 2", kind="Accepted")
        self.group = Group.objects.create(name="HOD")
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.post(reverse('home:login'), {'username': 'john', 'password': 'johnpassword'})

    def test_new_view(self):
        response = self.client.get(reverse('forms:transition-new', kwargs={"workflow_id": self.workflow.id}))
        self.assertEqual(response.status_code, 200)

        transition_count_before = Transition.objects.count()
        data = {'from_state': self.state_two.id, 'to_state': self.state_one.id, 'allowed_groups': [self.group.id]}
        response = self.client.post(reverse('forms:transition-new', kwargs={"workflow_id": self.workflow.id}), data)
        self.assertRedirects(response, reverse('forms:workflow-show', kwargs={"workflow_id": self.workflow.id}))
        self.assertEqual(Transition.objects.count(), transition_count_before + 1)

    def test_edit_view(self):
        transition = Transition.objects.create(workflow=self.workflow, from_state=self.state_one, to_state=self.state_two)
        response = self.client.get(reverse('forms:transition-edit', kwargs={"workflow_id": self.workflow.id, "transition_id": transition.id}))
        self.assertEqual(response.status_code, 200)

        new_data = {'from_state': self.state_two.id, 'to_state': self.state_one.id, 'allowed_groups': [self.group.id]}
        response = self.client.post(reverse('forms:transition-edit', kwargs={"workflow_id": self.workflow.id, "transition_id": transition.id}), new_data)
        self.assertRedirects(response, reverse('forms:workflow-show', kwargs={"workflow_id": self.workflow.id}))
        updated_transition = Transition.objects.get(pk=transition.id)
        self.assertEqual(updated_transition.from_state_id, self.state_two.id)

    def test_delete_view(self):
        transition = Transition.objects.create(workflow=self.workflow, from_state=self.state_one, to_state=self.state_two)
        transition_count_before = Transition.objects.count()

        response = self.client.get(reverse('forms:transition-delete', kwargs={"workflow_id": self.workflow.id, "transition_id": transition.id}))
        self.assertRedirects(response, reverse('forms:workflow-show', kwargs={"workflow_id": self.workflow.id}))
        self.assertEqual(Transition.objects.count(), transition_count_before - 1)
