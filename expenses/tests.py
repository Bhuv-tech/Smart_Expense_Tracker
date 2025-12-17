from django.test import TestCase
from django.urls import reverse


class URLNamesTest(TestCase):
    def test_charts_view_reverse(self):
        url = reverse('charts_view')
        self.assertEqual(url, '/charts/')


class ViewsRenderTest(TestCase):
    def test_expense_list_renders(self):
        resp = self.client.get(reverse('expense_list'))
        self.assertEqual(resp.status_code, 200)

    def test_logout_get_redirects(self):
        # create and login a user, then call logout via GET
        from django.contrib.auth.models import User

        user = User.objects.create_user('tester', 't@example.com', 'password')
        self.client.login(username='tester', password='password')
        resp = self.client.get(reverse('expense_logout'))
        # should redirect (302) after logout
        self.assertIn(resp.status_code, (302, 301))

    def test_accounts_login_renders(self):
        resp = self.client.get('/accounts/login/')
        # Should return 200 and include the login form
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Login', resp.content.decode())

    def test_logout_follow_redirects(self):
        # create and login a user, then call logout and follow redirects
        from django.contrib.auth.models import User

        user = User.objects.create_user('tester2', 't2@example.com', 'password')
        self.client.login(username='tester2', password='password')
        resp = self.client.get(reverse('expense_logout'), follow=True)
        # final response should be 200 and should not be an error page
        self.assertEqual(resp.status_code, 200, msg=f"status {resp.status_code}, redirect_chain={resp.redirect_chain}, final_path={resp.request.get('PATH_INFO')}")
        content = resp.content.decode()
        self.assertNotIn('This page isn’t working right now', content)
