import sys
import json
import random

from random import uniform, choice


class Controller(object):

    def __init__(self, sender, settings):
        self._current_time = 0
        self._time_limit = float("inf")
        self._max_depth = 10
        self._sender = sender
        self._settings = settings
        self._question = settings['question']
        self._answers = settings['answers']

    def __repr__(self):
        return '{}'.format(self._sender)

    def evaluate(self):
        self._invoke(self._sender, 1)
        print self._sender.replies

    def _invoke(self, user, depth):
        self._current_time += random.gauss(6, 1)

        if self._current_time > self._time_limit:
            return

        if depth > self._max_depth:
            return

        reply = uniform(0, 1)
        if reply < self._settings['reply_prob']:
            answer = user.answer(self._question, self._answers)
            if user.parent is not None:
                user.parent.replies.append(answer)

        for contact in user.contacts:
            forward = uniform(0, 1)
            if forward < self._settings['forwarding_prob']:
                self._invoke(contact, depth+1)

        if user.parent is not None:
            for item in user.replies:
                user.parent.replies.append(item)


class User(object):

    def __init__(self, user_info, contacts=None):
        self._contacts = [] if contacts is None else contacts
        self._user_info = user_info
        self._replies = []
        self._parent = None

    @property
    def replies(self):
        return self._replies

    @property
    def contacts(self):
        return self._contacts

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, user):
        self._parent = user

    def answer(self, question, answers):
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
        return self._user_info.name


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


class Parser(object):
    pass


def main(argv, *args, **kwargs):
    settings = {
        'question': 'How long is your dick?',
        'answers': ['Big', 'Small', 'Medium', 'Very small', 'XXL'],
        'reply_prob': 1.0,
        'forwarding_prob': 1.0 
    }

    roman = User(UserInfo('Roman', 25, 'Male'))
    gabe = User(UserInfo('Gabe', 27, 'Male'))
    ola = User(UserInfo('Ola', 25, 'Female'))
    victoria = User(UserInfo('Victoria', 22, 'Female'))

    gabe.add_contact(ola)

    roman.add_contact(gabe)
    roman.add_contact(victoria)

    controller = Controller(sender=roman, settings=settings)
    controller.evaluate()


if __name__ == '__main__':
    main(sys.argv)
