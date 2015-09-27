import json
import sys
import random
from random import uniform
import math

from utils import ContactsTree


class SimulationManager(object):

    def __init__(self, sender, settings):
        self._current_time = 0
        self._time_limit = settings['time_limit']
        self._max_depth = 10
        self._sender = sender
        self._settings = settings
        self._question = settings['question']
        self._answers = settings['answers']

    def __repr__(self):
        return '{}'.format(self._sender)

    def statistics(self):
        replies = self._sender.replies
        stats = dict((item, replies.count(item)) for item in replies)
        total_answers = float(sum(stats.values()))
        stats_relative = {
            k: math.floor(100*v/total_answers)
            for k, v in stats.iteritems()
        }
        return stats_relative

    def start_simulation(self):
        self._invoke(self._sender, 1)

    def _invoke(self, user, depth):
        self._current_time += random.gauss(1, 0.1)

        print 'Current time: {current_time}'.format(
            current_time=self._current_time
        )

        if self._current_time > self._time_limit:
            return

        if depth > self._max_depth:
            return

        reply = uniform(0, 1)
        if reply < self._settings['reply_prob']:
            answer = user.answer(self._answers)
            if user.parent is not None:
                print 'User {child} id={uid} replies to {parent} answer {answer}'.format(
                    uid=user.uid,
                    child=user.user_info.name,
                    parent=user.parent.user_info.name,
                    answer=answer
                )
                user.parent.replies.append(answer)

        for contact in user.contacts:
            forward = uniform(0, 1)
            if forward < self._settings['forwarding_prob']:
                print 'User {name} id={uid} forwards message'.format(
                    name=contact.user_info.name,
                    uid=contact.uid
                )
                self._invoke(contact, depth+1)

        if user.parent is not None:
            for item in user.replies:
                user.parent.replies.append(item)


def main(argv, *args, **kwargs):

    with open('config.json', 'r') as config_json:
        config = config_json.read()
        settings = json.loads(config)

    tree = ContactsTree(5)
    sender = tree.generate_tree()

    simulator = SimulationManager(sender=sender, settings=settings)
    simulator.start_simulation()

    stats = simulator.statistics()

    print '\nAggregated data...'
    for answer, votes in stats.iteritems():
        print 'Answer "{answer}" got {votes}% of votes'.format(
            answer=answer,
            votes=votes
        )


if __name__ == '__main__':
    main(sys.argv)
