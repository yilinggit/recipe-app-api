from django.test import TestCase, Client  # import test client that can make test requests 
from django.contrib.auth import get_user_model
from django.urls import reverse # allow us to generate urls for django admin page


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@fishdev.com',
            password='password123'
        )
        # Users client helper function - don't have to manually log the user in, client does it
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@fishdev.com',
            password='password123',
            name='Test User Full Name'
        )

    
    def test_user_listed_in_django_admin(self):
        """ Test that users are listed on user page"""
        """ These URLs are actually defined in the Django admin documentation which I will link to in the resources.
        And basically what this will do is it will generate the URL for our list user page. and the reason we
        use this reverse function instead of just typing the URL manually is because 
        if we ever want to change the URL in a future it means we don't have to go through and change it everywhere in our test because it should update
        automatically based on reverse."""

        url = reverse('admin:core_user_changelist')
        res = self.client.get(url) # use test client to perform a http get on the URL

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    
    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/

        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
    

    def test_create_user_page(self):
        """Test that create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    
