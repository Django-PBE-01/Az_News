from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class EmailLoginTests(TestCase):
	def test_registration_creates_user_that_authenticates_by_email(self):
		email = "registration-login@example.test"
		password = "Test-password-123!"

		response = self.client.post(
			reverse("accounts:register"),
			{
				"email": email,
				"first_name": "Test",
				"last_name": "User",
				"password": password,
				"confirm_password": password,
			},
		)

		self.assertRedirects(response, reverse("accounts:login"))
		user = User.objects.get(email=email)
		self.assertEqual(user.username, email)
		self.assertEqual(authenticate(email=email, password=password), user)

	def test_user_manager_populates_unique_username(self):
		email = "manager-login@example.test"
		user = User.objects.create_user(email=email, password="Test-password-123!")

		self.assertEqual(user.username, email)
		self.assertEqual(
			authenticate(email=email, password="Test-password-123!"), user
		)
