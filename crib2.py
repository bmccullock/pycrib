from collections import namedtuple, Counter, OrderedDict
import random
import itertools

class Card(namedtuple('Card', ['rank', 'suit'])):
	"""A tuple that represents a playing card in the form (RANK, SUIT)."""

	SUITS = {
		'H': ['Hearts', '♥'],
		'C': ['Clubs', '♣'],
		'D': ['Diamonds', '♦'],
		'S': ['Spades', '♠']
	}

	RANKS = { 
		1: ['Ace', 'A'], 
		11: ['Jack', 'J'],
		12: ['Queen', 'Q'],
		13: ['King', 'K']
	}
	
	def __new__(cls, rank, suit):
		return tuple.__new__(Card, (rank, suit))

	def __eq__(self, card):
		if self.rank == card.rank and self.suit == card.suit:
			return True
		else:
			return False

	def __str__(self):
		if self.rank in self.RANKS:
			rank = self.RANKS[self.rank][1]
		else:
			rank = self.rank
		return '{}{}'.format(rank, self.SUITS[self.suit][1])

	__repr__ = __str__

class Deck(object):
	"""An iterable collection of Card objects."""
	def __init__(self):
		super(Deck, self).__init__()
		self.cards = [Card(rank, suit) for suit in 'HCDS' for rank in range(1, 14)]

	def __getitem__(self, index):
		'''Access a card by its index in the deck/hand'''
		return self.cards[index]

	def __iter__(self):
		return iter(self.cards)

	def __len__(self):
		'''Return number of cards in the deck.'''
		return len(self.cards)

	def add(self, card):
		'''Add a card to the end (bottom) of the deck.'''
		self.cards.append(card)
		return

	def shuffle(self):
		'''Shuffle the deck in place.'''
		random.shuffle(self.cards)
		return

	def cut(self):
		'''Divide the deck in half and move card to top of deck. This is the
		starter or cut card.'''
		cards = []
		cut_card = self.cards.pop(random.randint(4, len(self.cards) - 5))
		cards.append(cut_card)
		cards.extend(self.cards)
		self.cards = cards

		return

	def draw(self):
		'''Return a single card from the top of the deck'''
		return self.cards.pop(0)

	def deal(self):
		'''Generate and return two hands of six cards by dealing in an alternating 
		fashion, as you would in real life. Return both hands as a list.'''
		hand1, hand2 = [], []
		for i in range(1,13):
			if i % 2 == 0:
				hand1.append(self.draw())
			else:
				hand2.append(self.draw())

		return [hand1, hand2]

	def return_hand(self, hand):
		'''Return all cards in a hand to the deck.'''
		self.cards.extend(hand)

class Hand(Deck):
	"""docstring for Hand"""
	def __init__(self):
		super(Hand, self).__init__()
		self.cards = []

	def __str__(self):
		return ' '.join(map(str, self.cards))

	def discard(self, crib):
		'''Discard two cards to the crib, choosing the two cards that result in 
		the highest point score for the remaining four cards.

		TODO:
		  >>Adjust discard strategy according to which player is currently the 
			dealer (has the crib).
		  >>Weight and apply various discard strategies.

		'''

		# check resulting score when discarding 
		discard_results = []
		for combo in itertools.combinations(self.cards, 2):
			test_hand = Hand()
			test_hand.cards = [card for card in self.cards if card not in combo]
			result = [Game().score_hand(test_hand)[0], combo]
			discard_results.append(result)
		
		discard_results.sort(key = lambda x: x[0], reverse = True)
		
		for card in discard_results[0][1]:
			index = self.cards.index(card)
			crib.add(self.cards.pop(index))

		return

	def ranks(self):
		'''Return a list containing only numerical ranks of cards in hand'''
		return [c[0] for c in self.cards]

	def suits(self):
		'''Return a list containing only suits of cards in hand.'''
		return [c[1] for c in self.cards]

	def values(self):
		'''Return a list containing only the point values of cards in hand'''
		values_list = []
		for c in self.ranks():
			if c > 10:
				values_list.append(10)
			else:
				values_list.append(c)
		return values_list

	
	def fifteens(self):
		'''Return a list containing all card combinations that total 15. Since 
		cards are handled as int values, face cards will need to be converted to 
		there point values of 10.
		'''
		fifteens = []

		for i in range(2, 5):
			c = itertools.combinations(self.values(), i)
			for combo in c:
				if sum(combo) == 15:
					fifteens.append(combo)
		return fifteens

	def flush(self):
		'''Return True if all cards in hand match by suit.'''
		has_flush = False
		for i in Counter(self.suits()).most_common(4):
			if i[1] == 4 or i[1] == 5:
				has_flush = True
		return has_flush

	def pairs(self):
		'''Return a list containing all matching pairs (by rank)'''
		return [c for c in itertools.combinations(self.ranks(), 2) if c[0] == c[1]]

	def runs(self):
		'''Return longest sequence of 3 or more cards.

		TODO:
			Adapt to handle Aces high or low
		'''
		poss_runs = []
		ranks = [c.rank for c in self.cards]
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
		elif len(self.cards) >= 4 and fours:
			for run in fours:
				runs.append(run)
			pass
		elif threes:
			for run in threes:
				runs.append(run)
			pass
		return runs

	def his_nobs(self, starter):
		'''Return True if hand has JACK of same suit as starter card'''
		for card in [c for c in self.cards if c.rank == 11]:
			if card.suit == starter.suit:
				return True
		return False

	__repr__ = __str__
		

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
		print(self.winner)
		while (self.score['p1'] < 121) and (self.score['p2'] < 121):
			
			print('Round: {}'.format(round_num))
			# Play a round
			round = self.round(round_num)
			for p in self.score.keys():
				self.score[p] += round[p]['score']
			self.history[round_num] = round
			round_num += 1


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
		self.the_crib(p1_hand, p2_hand, crib)

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
		breakdown = {
			'fifteens': 0,
			'pairs': 0,
			'runs': 0,
			'flush': 0,
			'nobs': 0
		}

		breakdown['fifteens'] += 2 * len(hand.fifteens())
		# score pairs
		breakdown['pairs'] += 2 * len(hand.pairs())
		# score runs
		runs_list = hand.runs()
		for run in runs_list:
			breakdown['runs'] += len(run)
		# score flush
		if hand.flush():
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

	def the_crib(self, p1_hand, p2_hand, crib):
		'''Each player looks at his six cards and discards two of them to the 
		crib.'''
		for hand in [p1_hand, p2_hand]:
			hand.discard(crib)
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

