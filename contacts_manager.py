from random import choice, Random
import math
from simulation import UserInfo


class ContactsManager(object):
    _names = ['Joe', 'Sam', 'Gabe', 'Jessy', 'Mike']
    _genders = ['M', 'F']

    def __init__(self):
        pass

    def _contacts_generator(self, count, age_range):
        random = Random()
        min_age, max_age = age_range
        for i in xrange(count):
            user_info = UserInfo(
                choice(self._names),
                math.floor(random.uniform(min_age, max_age)),
                choice(self._genders)
            )
            yield user_info

    def generate_contacts(self, count, age_range=(15, 60)):
        contacts = self._contacts_generator(count, age_range)
        return [contact for contact in contacts]


class ContactsTree(object):
    _contacts = []

    def __init__(self, depth):
        pass


class ContactsTreeVisualizer(object):
    pass