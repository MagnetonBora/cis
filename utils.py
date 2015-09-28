from random import choice, Random, randint
import math
import string
import networkx as nx
import matplotlib.pyplot as plt


def read_names(file_path):
    with open(file_path, 'r') as input_file:
        names = input_file.readlines()
    return names

def visualize_graph(nodes):
    G = nx.Graph()

    for node in nodes:
        for contact in node['contacts']:
            G.add_edge(node['id'], contact.uid)

    nx.draw_spectral(G)
    plt.show()

class User(object):

    def __init__(self, user_info, contacts=None):
        self._uid = self._generate_uid(8)
        self._contacts = [] if contacts is None else contacts
        self._user_info = user_info
        self._replies = []
        self._parent = None

    def _generate_uid(self, length):
        symbols = [choice(string.ascii_letters + string.digits) for i in xrange(length)]
        return string.join(symbols, '')

    def _traverse(self, root, users):
        item = dict(
            id=root.uid,
            name=root.user_info.name,
            contacts=root.contacts
        )
        users.append(item)
        for contact in root.contacts:
            self._traverse(contact, users)
        return users

    def traverse(self):
        return self._traverse(self, [])

    def to_dict(self):
        info = self._user_info.to_dict()
        info.update(dict(uid=self._uid))
        return info

    @property
    def user_info(self):
        return self._user_info

    @property
    def uid(self):
        return self._uid

    @property
    def replies(self):
        return self._replies

    @property
    def contacts(self):
        return self._contacts

    @contacts.setter
    def contacts(self, contacts_collection):
        if len(self._contacts) == 0:
            self._contacts = contacts_collection
        else:
            for contact in contacts_collection:
                self._contacts.append(contact)

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, user):
        self._parent = user

    def answer(self, answers):
        return choice(answers)

    def add_contact(self, contact=None):
        if contact is not None:
            contact.parent = self
            self._contacts.append(contact)

    def add_contacts(self, contacts=None):
        if contacts is not None:
            for contact in contacts:
                self.add_contact(contact)

    def __repr__(self):
        return "Name: {name}, id: {id}".format(
            name=self._user_info.name,
            id=self._uid
        )


class UserInfo(object):

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __repr__(self):
        user_string = 'User: {name}, age: {age}, gender: {gender}'.format(
            name=self.name,
            age=self.age,
            gender=self.gender
        )
        return user_string

    def to_dict(self):
        return self.__dict__


class ContactsManager(object):
    _names = []
    _genders = ['M', 'F']

    def __init__(self):
        self._names = read_names('data/names.dat')

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
        user.contacts = self.manager.generate_contacts(randint(3, 5))
        if depth >= 0:
            for contact in user.contacts:
                contact.parent = user
                self._generate_tree(contact, depth-1)

    def generate_tree(self):
        user = self.manager.generate_contacts(1)[0]
        self._generate_tree(user, self.depth-1)
        return user

