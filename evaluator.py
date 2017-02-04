'''

'''
import itertools
from collections import Counter

class Evaluator(object):
	"""docstring for Evaluator"""
	def __init__(self, hand_obj):
		super(Evaluator, self).__init__()
		self.hand = hand_obj

	def score(self):
		breakdown = {
			'fifteens': 2 * len(self.fifteens()),
			'pairs': 2 * len(self.pairs()),
			'runs': sum([len(r) for r in self.runs()]),
			'flush': 0,
			'nobs': 0
		}

		if self.flush():
			breakdown['flush'] += 4

		num_score = sum([breakdown[key] for key in breakdown.keys()])
		return [num_score, breakdown]

	def fifteens(self):
		'''Return a list containing all card combinations that total 15. Since 
		cards are handled as int values, face cards will need to be converted to 
		there point values of 10.
		'''
		fifteens = []

		for i in range(2, 5):
			c = itertools.combinations(self.hand.values(), i)
			for combo in c:
				if sum(combo) == 15:
					fifteens.append(combo)
		return fifteens

	def flush(self):
		'''Return True if all cards in hand match by suit.'''
		has_flush = False
		for i in Counter(self.hand.suits()).most_common(4):
			if i[1] == 4 or i[1] == 5:
				has_flush = True
		return has_flush

	def pairs(self):
		'''Return a list containing all matching pairs (by rank)'''
		return [c for c in itertools.combinations(self.hand.ranks(), 2) if c[0] == c[1]]

	def runs(self):
		'''Return longest sequence of 3 or more cards.

		TODO:
			Adapt to handle Aces high or low
		'''
		poss_runs = []
		ranks = [c.rank for c in self.hand.cards]
		for i in range(5, 2, -1):
			combos = [sorted(list(set(c))) for c in itertools.combinations(ranks, i)]

			for c in combos:
				if len(c) >= i:
					if len(c) == (c[-1] - c[0] + 1):
						poss_runs.append(c)

		fives = [r for r in poss_runs if len(r) == 5]
		fours = [r for r in poss_runs if len(r) == 4]
		threes = [r for r in poss_runs if len(r) == 3]

		runs = []

		if fives:
			for run in fives:
				runs.append(run)
			pass
		elif len(self.hand.cards) >= 4 and fours:
			for run in fours:
				runs.append(run)
			pass
		elif threes:
			for run in threes:
				runs.append(run)
			pass
		return runs

	def his_nobs(self):
		'''Return True if hand has JACK of same suit as starter card'''
		for card in [c for c in self.hand.cards if c.rank == 11]:
			if card.suit == starter.suit:
				return True
		return False
		
		