from unittest import TestCase
from contacts_manager import ContactsManager


class ContactsManagerTest(TestCase):

    def setUp(self):
        self.manager = ContactsManager()

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
