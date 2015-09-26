import sys
import random
from random import uniform

from contacts_manager import ContactsTree


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

    def start_simulation(self):
        self._invoke(self._sender, 1)

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
                print 'User id: {uid} {child} replies to {parent}'.format(
                    uid=user.uid,
                    child=user.user_info.name,
                    parent=user.parent.user_info.name
                )
                user.parent.replies.append(answer)

        for contact in user.contacts:
            forward = uniform(0, 1)
            if forward < self._settings['forwarding_prob']:
                self._invoke(contact, depth+1)

        if user.parent is not None:
            for item in user.replies:
                user.parent.replies.append(item)


def main(argv, *args, **kwargs):
    settings = {
        'question': 'How long is your dick?',
        'answers': ['Big', 'Small', 'Medium', 'Very small', 'XXL'],
        'reply_prob': 1.0,
        'forwarding_prob': 1.0 
    }

    tree = ContactsTree(2)
    sender = tree.generate_tree()

    controller = Controller(sender=sender, settings=settings)
    controller.start_simulation()

    print sender.replies


if __name__ == '__main__':
    main(sys.argv)
