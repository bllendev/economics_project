from django.test import TestCase
from django.urls import reverse
from users.tests.factories import (
    CustomUserFactory,
)


class SignupPageTests(TestCase):

    TEST_EMAIL = "testuser@email.com"
    TEST_USERNAME = "testuser"

    def setUp(self):
        self.test_user = CustomUserFactory.create(username=self.TEST_USERNAME)
        url = reverse("account_signup")
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "account/signup.html")
        self.assertContains(self.response, "Sign Up")
