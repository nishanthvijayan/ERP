from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from forms.models import Workflow

class WorkflowEntryViewTests(TestCase):
    def setUp(self):
        self.workflow = Workflow.objects.create(name="Example Workflow", description="This is a test workflow")
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.post(reverse('home:login'), {'username': 'john', 'password': 'johnpassword'})

    def test_index_view(self):
        response = self.client.get(reverse('forms:workflow-entry-index', kwargs={"workflow_id": self.workflow.id}))
        self.assertEqual(response.status_code, 200)

    def test_new_view(self):
        response = self.client.get(reverse('forms:workflow-entry-new', kwargs={"workflow_id": self.workflow.id}))
        self.assertEqual(response.status_code, 200)
        # TODO Actually creating a workflow entry
