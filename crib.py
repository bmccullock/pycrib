from collections import namedtuple, Counter, OrderedDict
import itertools

from deck import Card, Deck, Hand
from evaluator import Evaluator



class Game(object):
	"""Represents an entire game of cribbage between two players. A game consists 
	of as many rounds as needed for one player to exceed the final score of 121.
	"""

	WINNING_SCORE = 121

	def __init__(self):
		super(Game, self).__init__()
		self.deck = Deck()
		self.score = dict.fromkeys(['p1', 'p2'], 0) # Should this be a view?
		self.history = OrderedDict()
		self.winner = True in [self.score[p] >= 121 for p in self.score.keys()]

	def run(self):
		'''Simulate a cribbage game, playing rounds until one player reaches the 
		winning score of 121 points.

		'''
		round_num = 1
		
		while (self.score['p1'] < 121) and (self.score['p2'] < 121):
			
			print('Round: {}'.format(round_num))
			# Play a round
			round = self.round(round_num)
			for p in self.score.keys():
				self.score[p] += round[p]['score']
			self.history[round_num] = round
			round_num += 1
		print(self.winner)

	def round(self, round_num):
		'''Plays a single round of cribbage. Deals two hands, discards to the 
		crib, scores hands (and crib), and update the score for each player.

		TODO:
			Pegging

		'''
		round = {
			'p1': {
				'hand': [], 'score': 0, 'brkdwn': None, 'crib': False
			},
			'p2': {
				'hand': [], 'score': 0, 'brkdwn': None, 'crib': False
			},
			'starter': None
		}

		if round_num % 2 == 0:
			round['p2']['crib'] = True
		else:
			round['p1']['crib'] = True


		# Shuffle deck of cards and deal two hands
		self.deck.shuffle()
		p1_hand, p2_hand, crib = Hand(), Hand(), Hand()
		self.deal(p1_hand, p2_hand)

		# Discard phase...send two cards to crib
		self.the_discard(p1_hand, p2_hand, crib)

		round['p1']['hand'] = p1_hand
		round['p2']['hand'] = p2_hand

		# Cut deck and reveal the starter
		self.deck.cut()
		starter = self.deck[0]
		round['starter'] = starter

		p1_hand.cards.append(starter)
		p2_hand.cards.append(starter)

		# The show
		self.the_play(p1_hand, p2_hand)


		# Save round to game history and update total score
		p1_score = self.score_hand(p1_hand)
		round['p1']['score'] += p1_score[0]
		round['p1']['brkdwn'] = p1_score[1]

		p2_score = self.score_hand(p2_hand)
		round['p2']['score'] += p2_score[0]
		round['p2']['brkdwn'] = p2_score[1]

		for p in ['p1', 'p2']:
			if round[p]['crib'] == True:
				round[p]['score'] += self.score_hand(crib)[0]

		# Return all cards to deck
		for hand in [p1_hand, p2_hand, crib]:
			self.deck.return_hand(hand)

		return round

	def score_hand(self, hand):
		'''Given a Hand(), return a list with the total points score for the 
		hand and a dict containing the breakdown by scoring category:

			score = [num_score, {breakdown}]

		FIFTEENS:	2 pts per combo totalling 15
		PAIRS: 		2 pts per pair of same rank
		RUNS:		1 pt per card in run of 3+
		FLUSH:		4 pts for four of same suit in hand
		HIS NOBS:	1 pt for jack matching suit of starter
		'''
		ev = Evaluator(hand)
		breakdown = {
			'fifteens': 2 * len(ev.fifteens()),
			'pairs': 2 * len(ev.pairs()),
			'runs': sum([len(r) for r in ev.runs()]),
			'flush': 0,
			'nobs': 0
		}

		if ev.flush():
			breakdown['flush'] += 4

		num_score = sum([breakdown[key] for key in breakdown.keys()])
		return [num_score, breakdown]

	def deal(self, p1_hand, p2_hand):
		'''Deal six cards to each hand from the top of the deck, alternating 
		between each player as you would deal cards in real life.'''
		for i in range(1,13):
			if i % 2 == 0:
				p1_hand.add(self.deck.draw())
			else:
				p2_hand.add(self.deck.draw())
		return

	def the_discard(self, p1_hand, p2_hand, crib):
		'''Each player looks at his six cards and discards two of them to the 
		crib. Choose the two cards that result in the highest score for the 
		remaining four cards.
		
		TODO:
		  >>Adjust discard strategy according to which player is currently the 
			dealer (has the crib).
		  >>Weight and apply various discard strategies.
		'''

		for hand in [p1_hand, p2_hand]:
			ev = Evaluator(hand)

			discard_results = []
			# check each 2 card combination
			for combo in itertools.combinations(hand.cards, 2):
				test_hand = Hand()
				test_hand.cards = [card for card in hand.cards if card not in combo]
				result = [ev.score()[0], combo]
				discard_results.append(result)
			
			discard_results.sort(key = lambda x: x[0], reverse = True)
			
			for card in discard_results[0][1]:
				index = hand.cards.index(card)
				crib.add(hand.cards.pop(index))

		return

	def the_play(self, p1_hand, p2_hand):
		'''The non-dealer (aka "pone") shows a card to begin the play and the 
		dealer follows accordingly. The goal is to achieve running totals of 15 
		and 31. 

		If a player is unable to add a card without exceeding 31, he says "go" 
		and his opponent "pegs" 1 point.

		** This requires that information about who is currently the dealer gets 
		passed into the function

		'''
		play_score = [0, 0]

		ranks = sorted(p1_hand.ranks()), sorted(p2_hand.ranks())

		# run until there are no cards in either hand
		total = 0
		while len(ranks[0]) > 0 or len(ranks[1]) > 0:
			for i in ranks:
				if len(i) > 0:
					if ranks.index(i) == 0:
						print('Player 1 Cards: {}'.format(i))
					else:
						print('Player 2 Cards: {}'.format(i))
					
					if total + i[0] <= 31:
						# Check each card against the total. If equals 15 or 31,
						# choose that card
						total += i[0]
						print(i[0])
						print('Total: {}'.format(total))
						del i[0]

						if total == 15:
							play_score[ranks.index(i)] += 2
							print('Fifteen for two.')
						elif total == 31:
							print('Total: {}'.format(total))
							print('Thirty-one for two.')

					else:
						
						total = 0	
		print(play_score)
		return

	def the_show(self):
		'''Game phase where each player scores their five cards (hand + starter)  
		for fifteens, pairs, runs, etc. Hands are counted in order: non-dealer, 
		dealer's hand, crib. This order is important near the end of the game, as 
		the non-dealer has the opportunity to "count out" and win before the 
		dealer has a chance to count, even though the dealer's total would have 
		exceeded his opponent's score.
		return'''


if __name__ == '__main__':
	g = Game()
	g.run()

