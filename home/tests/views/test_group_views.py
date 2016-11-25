from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group

class GroupViewTests(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="HOD")
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.post(reverse('home:login'), {'username': 'john', 'password': 'johnpassword'})

    def test_new_view(self):
        group_count_before = Group.objects.count()
        response = self.client.get(reverse('home:group-new'))
        self.assertEqual(response.status_code, 200)

        data = {'name': 'mary jane'}
        response = self.client.post(reverse('home:group-new'), data)
        self.assertEqual(Group.objects.count(), group_count_before + 1)
        self.assertRedirects(response, reverse('home:group-index'))

    def test_edit_view(self):
        response = self.client.get(reverse('home:group-edit', kwargs={"group_id": self.group.id}))
        self.assertEqual(response.status_code, 200)
        new_data = {'name': 'mary jane'}
        response = self.client.post(reverse('home:group-edit', kwargs={"group_id": self.group.id}), new_data)

        updated_group_element = Group.objects.get(pk=self.group.id)
        self.assertEqual(updated_group_element.name, 'mary jane')
        self.assertRedirects(response, reverse('home:group-show', kwargs={"group_id": self.group.id}))

    def test_delete_view(self):
        group_count_before = Group.objects.count()
        response = self.client.get(reverse('home:group-delete', kwargs={"group_id": self.group.id}))
        self.assertEqual(Group.objects.count(), group_count_before - 1)
        self.assertRedirects(response, reverse('home:group-index'))

    def test_index_view(self):
        response = self.client.get(reverse('home:group-index'))
        self.assertEqual(response.status_code, 200)

    def test_show_view(self):
        response = self.client.get(reverse('home:group-show', kwargs={"group_id": self.group.id}))
        self.assertEqual(response.status_code, 200)

    def test_toggle_view(self):
        data = {"username": self.user.username}
        response = self.client.post(reverse('home:group-user-toggle', kwargs={"group_id": self.group.id}), data)
        check_user_exists = Group.objects.filter(id=self.user.id).exists()
        self.assertEqual(check_user_exists, True)
