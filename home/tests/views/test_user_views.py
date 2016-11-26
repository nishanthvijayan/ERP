from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserViewTests(TestCase):

    '''
    Class for test functions of User Views.
    '''

    def setUp(self):
        '''
        Test function to setup a sample database before each test.
        '''

        self.user = User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.post(reverse('home:login'), {
                         'username': 'john', 'password': 'johnpassword'})

    def test_new_view(self):
        '''
        Test function for adding a new user.
        '''

        user_count_before = User.objects.count()
        response = self.client.get(reverse('home:user-new'))
        self.assertEqual(response.status_code, 200)

        data = {
            'username': 'mary', 'first_name': 'mary', 'last_name': 'jane',
            'email': 'maryjane@spider.com', 'password1': 'maryjane123', 'password2': 'maryjane123'
        }
        response = self.client.post(reverse('home:user-new'), data)
        self.assertEqual(User.objects.count(), user_count_before + 1)
        self.assertRedirects(response, reverse('home:user-index'))

    def test_edit_view(self):
        '''
        Test function for editing the details of an existing user.
        '''

        response = self.client.get(
            reverse('home:user-edit', kwargs={"user_id": self.user.id}))
        self.assertEqual(response.status_code, 200)
        new_data = {'username': 'mary123',
                    'first_name': 'jane', "last_name": 'mary'}
        response = self.client.post(
            reverse('home:user-edit', kwargs={"user_id": self.user.id}), new_data)
        updated_user_element = User.objects.get(pk=self.user.id)
        self.assertEqual(updated_user_element.username, 'mary123')
        self.assertRedirects(response, reverse('home:user-index'))

    def test_delete_view(self):
        '''
        Test function for deleting a user.
        '''

        user_count_before = User.objects.count()
        self.client.get(reverse('home:user-delete',
                                kwargs={"user_id": self.user.id}))
        self.assertEqual(User.objects.count(), user_count_before - 1)
        # TODO: self.assertRedirects(response, reverse('home:user-index'))

    def test_index_view(self):
        '''
        Test function for user list view.
        '''

        response = self.client.get(reverse('home:user-index'))
        self.assertEqual(response.status_code, 200)
