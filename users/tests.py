import hmac
import hashlib
import json
import time
from rest_framework.test import APITestCase
from django.urls import reverse
from django.conf import settings
from materials.models import Course
from rest_framework import status
from users.models import User
from users.views import PaymentsViewSet
from users.stripe import stripe


class StripeIntegrationTests(APITestCase):
    def setUp(self):
        email = "stripe_test@mail.ru"
        password = "stripe12345"
        self.user = User.objects.create_user(email=email, password=password, username='stripe_test')
        self.course = Course.objects.create(name="Python", description="sbj")
        token = self.client.post(reverse("users:login"), {"email": email, "password": password}).json()["access"]
        self.headers = {"Authorization": f"Bearer {token}"}

    def test_create_payment_intent(self):
        url = reverse("users:create_payment")

        data = {
            "subject": "course",
            "course_id": self.course.id,
            "amount": 1000,
        }
        response = self.client.post(url, data, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stripe_webhook(self):
        url = reverse("users:stripe_webhook")
        
        data = {
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "id": "pi_123456789",
                    "amount": 1000,
                    "currency": "usd"
                }
            }
        }
        
        secret = settings.STRIPE_WEBHOOK_SECRET
        payload = json.dumps(data)
        timestamp = str(int(time.time()))


        signed_payload = f"{timestamp}.{payload}".encode("utf-8")
        signature = hmac.new(secret.encode(), signed_payload, hashlib.sha256).hexdigest()
        
        stripe_signature = f"t={timestamp},v1={signature}"

        response = self.client.post(
            url,
            data=payload,
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE=stripe_signature
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)

    def tearDown(self):
        pass
