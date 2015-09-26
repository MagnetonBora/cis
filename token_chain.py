
"""
Generating of identification token. The tokes is a random string
of length 8. The alphabet of symbols to be generated is a set of
small and capital english letters plus numbers from 0 to 9.
"""

'''

{
	meta: {
		'id': 'vAdZ2HFe',
		'ttl': '2015-08-16T23:59:59.000000',
		'timestamp': '2015-07-16T22:48:54.588762',
		'prevNodes': ['H9dzpTuV', 'hE0J7aSX'],
		'maxNumOfHops': 10
		'profile': {
			'name': 'Joe',
			'age': 24,
			'gender': 'M',
			'location': 'Warsaw'
		}
	},
	answers: ['good', 'bad', 'medium'],
	content: 'What do you think about Terminator 5?'
}

'''

import random
import string

TOKEN_LENGTH = 8


def generate_token(length):
    symbols = [random.choice(string.ascii_letters + string.digits) for i in xrange(length)]
    return string.join(symbols, '')

if __name__ == '__main__':
	for i in xrange(10):
		print generate_token(TOKEN_LENGTH)
