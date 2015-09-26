from unittest import TestCase
from mock import patch
from utils import ContactsManager


class ContactsManagerTest(TestCase):

    def setUp(self):
        self.read_names = patch('utils.read_names').start()
        self.read_names.return_value = ['Sam', 'Joe', 'Sue']
        self.manager = ContactsManager()

    def tearDown(self):
        self.read_names.stop()

    def test_generates_random_contacts_set(self):
        contacts = self.manager.generate_contacts(5)

        self.assertEquals(5, len(contacts))

    def test_generates_contacts_with_given_age_range(self):
        min_age, max_age = 10, 60

        contact = self.manager.generate_contacts(5)[0]

        self.assertLessEqual(contact.to_dict()['age'], max_age)
        self.assertGreaterEqual(contact.to_dict()['age'], min_age)

    def test_generates_proper_contact(self):
        contact = self.manager.generate_contacts(1)[0]

        self.assertIn('name', contact.to_dict())
        self.assertIn('gender', contact.to_dict())
        self.assertIn('age', contact.to_dict())
