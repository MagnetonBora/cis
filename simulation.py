import json
import sys
import random
import click
import math
import pylab

from random import uniform
from pylab import figure
from matplotlib.pyplot import hist
from utils import User, ContactsTree, visualize_graph


def generate_age_ranges(count=100, mu=0, sigma=1):
    return [mu + sigma * random.gauss(0, 1) for i in xrange(count)]


class SimulationManager(object):

    def __init__(self, sender, settings):
        self._current_time = 0
        self._time_limit = settings['time_limit']
        self._max_depth = 10
        self._sender = sender
        self._settings = settings
        self._question = settings['question']
        self._answers = settings['answers']
        self._avg_request_number = 0
        self._use_profile_spreading = settings.get('use_profile_spreading', False)

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

    def average_request_number(self):
        return self._avg_request_number

    def start_simulation(self):
        self._invoke(self._sender, 1)

    def _invoke(self, user, depth):
        self._current_time += random.gauss(1, 0.1)
        self._avg_request_number += 1

        print 'Current time: {current_time}'.format(
            current_time=self._current_time
        )

        if self._current_time > self._time_limit:
            return

        if depth > self._max_depth:
            return

        reply = -math.log(random.random() + 0.0001)/user.user_info.age
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
            if self._use_profile_spreading and contact.user_info.age > user.user_info.age:
                continue

            forward = -math.log(random.random() + 0.0001)/contact.user_info.age
            if forward < self._settings['forwarding_prob']:
                print 'User {name} id={uid} forwards message'.format(
                    name=contact.user_info.name,
                    uid=contact.uid
                )
                self._invoke(contact, depth+1)

        if user.parent is not None:
            for item in user.replies:
                user.parent.replies.append(item)


def serializer(obj):
    if isinstance(obj, User):
        return obj.to_dict()


@click.command()
@click.option(
    '--show-age-clusterization',
    is_flag=True,
    default=False,
    help='Show age clusterization histogram'
)
@click.option(
    '--show-contacts-tree',
    is_flag=True,
    default=False,
    help='Show contacts tree'
)
@click.option(
    '--show-total-statistics',
    is_flag=True,
    default=False,
    help='Show total statistics'
)
@click.option(
    '--show-all-contacts',
    is_flag=True,
    default=False,
    help='Show all contacts'
)
@click.option(
    '--use-profile-spreading',
    is_flag=True,
    default=False,
    help='Use profile spreading'
)
def main(show_age_clusterization, show_contacts_tree,
         show_total_statistics, show_all_contacts,
         use_profile_spreading):

    with open('config.json', 'r') as config_json:
        config = config_json.read()
        settings = json.loads(config)

    tree = ContactsTree(settings['depth'], settings['age_params'])
    sender = tree.generate_tree()
    settings.update(dict(use_profile_spreading=use_profile_spreading))
    
    simulator = SimulationManager(sender=sender, settings=settings)
    simulator.start_simulation()
    nodes = sender.traverse()

    if show_total_statistics:
        stats = simulator.statistics()
        click.echo('\nAverage request number: {}'.format(simulator.average_request_number()))
        click.echo('\nAggregated data...')
        for answer, votes in stats.iteritems():
            click.echo(
                'Answer "{answer}" got {votes}% of votes'.format(
                    answer=answer,
                    votes=votes
                )
            )
    
    if show_contacts_tree:
        figure(1)
        visualize_graph(nodes)

    if show_age_clusterization:
        figure(2)
        hist(
            generate_age_ranges(1000, settings['age_params']['avg_age'], settings['age_params']['age_dev']),
            bins=50
        )
        pylab.show()

    if show_all_contacts:
        json_nodes = json.dumps(nodes, default=serializer, indent=4)
        click.echo('\nContacts tree:\n{}'.format(json_nodes))


if __name__ == '__main__':
    main()
