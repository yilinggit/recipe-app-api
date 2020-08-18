from django.test import TestCase, Client
# import test client that can make test requests
from django.contrib.auth import get_user_model
from django.urls import reverse
# allow us to generate urls for django admin page
# https://www.mlr2d.org/contents/djangorestapi/05_modifying_djangoadmininterface


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@fishdev.com',
            password='password123'
        )
        # Users client helper function -
        # don't have to manually log the user in, client does it
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@fishdev.com',
            password='password123',
            name='Test User Full Name'
        )

    def test_user_listed_in_django_admin(self):
        """ Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        # use test client to perform a http get on the URL

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
