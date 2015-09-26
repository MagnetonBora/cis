from random import choice, Random, randint
import math

from simulation import UserInfo, User


class ContactsManager(object):
    _names = ['Joe', 'Sam', 'Gabe',
              'Jessy', 'Mike', 'Ola', 'Jack', 'Joe']
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
            yield User(user_info)

    def generate_contacts(self, count, age_range=(15, 60)):
        contacts = self._contacts_generator(count, age_range)
        return [contact for contact in contacts]


class ContactsTree(object):

    def __init__(self, depth):
        self.depth = depth
        self.manager = ContactsManager()

    def _generate_tree(self, user, depth):
        if depth != 0:
            for contact in user.contacts:
                self._generate_tree(contact, depth-1)
        user.contacts = self.manager.generate_contacts(randint(5, 8))

    def generate_tree(self, depth):
        user = self.manager.generate_contacts(1)[0]
        self._generate_tree(user, depth-1)
        return user


class ContactsTreeVisualizer(object):
    pass


if __name__ == '__main__':
    pass
