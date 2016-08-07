from django.test import TestCase, Client
import unittest

from skaba.models import User, Event, Guild

TEST_EVENT_NAME = 'Test event'
TEST_EVENT_DESC = 'This is an event for testing'
TEST_EVENT_SLUG = 'test-event'
TEST_EVENT_POINTS = 10
TEST_EVENT_GUILD = 1

TEST_ADMIN_PASSWORD = 'password'
TEST_ADMIN_USERNAME = 'test_admin1'

try:
	test_admin = User.objects.create_superuser(TEST_ADMIN_USERNAME, 'test@example.com', TEST_ADMIN_PASSWORD)
except:
	pass
class EventTest(unittest.TestCase):
	def setUp(self):
		self.client = Client()

	def create_mock_event(self):
		self.event = Event.objects.create(name=TEST_EVENT_NAME, 
			description=TEST_EVENT_DESC,
			slug=TEST_EVENT_SLUG,
			points=TEST_EVENT_POINTS,
			guild=TEST_EVENT_GUILD)

	def test_create(self):
		self.client.login(username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD)
		response = self.client.post('/admin/events/add/', 
			{
				'name': TEST_EVENT_NAME,
				'description': TEST_EVENT_DESC,
				'slug': TEST_EVENT_SLUG,
				'points': TEST_EVENT_POINTS,
				'guild': TEST_EVENT_GUILD
			})
		self.assertEqual(response.status_code, 302)
		self.assertIsNotNone(Event.objects.filter(slug=TEST_EVENT_SLUG))