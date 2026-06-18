from django.test import TestCase


class IntegrationTest(TestCase):
    def test_ping(self):
        response = self.client.get('/ping/')
        self.assertEqual(response.status_code, 200)
