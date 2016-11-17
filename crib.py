from collections import Counter, namedtuple
import itertools
import random

class Card(namedtuple('Card', ['rank', 'suit'])):

	SUITS = {'H': 'Hearts', 'D': 'Diamonds', 'C': 'Clubs', 'S': 'Spades'}
	NAMES = { 'A': 'Ace', 'X': '10', 'J': 'Jack', 'Q': 'Queen', 'K': 'King'}
	VALUES = { 'A': 1, 'J': 10, 'Q': 10, 'K': 10}

	def __new__(cls, rank, suit):
		if rank == 'X':
			rank = 10
		return tuple.__new__(Card, (rank, suit))

	def __eq__(self, card):
		if self.rank == card.rank and self.suit == card.suit:
			return True
		else:
			return False

	def __repr__(self):
		return '({}, {})'.format(self.rank, self.suit)

	def __str__(self):
		if self.rank in self.NAMES:
			name = self.NAMES[self.rank]
		else:
			name = self.rank
		return '{} of {}'.format(name, self.SUITS[self.suit])

	def value(self):
		if self.rank in self.VALUES:
			return self.VALUES[self.rank]
		else:
			return int(self.rank)

class Deck:

	def __init__(self):
		self.cards = [Card(rank, suit) for suit in 'HDCS' for rank in 'A23456789XJQK']
		self.count = len(self)

	def __len__(self):
		return len(self.cards)

	def __iter__(self):
		return iter(self.cards)

	def shuffle(self):
		random.shuffle(self.cards)
		return

	def cut(self):
		cut_index = round(len(self.cards) / 2) #Assume an even cut of deck for now
		cut_card = self.cards.pop(cut_index)
		self.cards.insert(0, cut_card)
		return

	def add_card(self, card):
		self.cards.append(card)
		return

	def deal(self, player_1, player_2):
		# Deal two hands, alternating
		for i in range(1,13):
			if i % 2 == 0:
				player_1.add_card(self.cards.pop(0))
			else:
				player_2.add_card(self.cards.pop(0))

	def numerical_ranks(self):
		num_ranks = []
		for rank in [c[0] for c in self.cards]:
			if rank == 'A':
				num_ranks.append(1)
			elif rank == 'J':
				num_ranks.append(11)
			elif rank == 'Q':
				num_ranks.append(12)
			elif rank == 'K':
				num_ranks.append(13)
			else:
				num_ranks.append(int(rank))
		return sorted(num_ranks)

class Hand(Deck):

	def __init__(self):
		self.cards = []
		self.score = {
			'pair': 0,
			'triplet': 0,
			'fourkind': 0,
			'flush': 0
		}

	def card_count(self):
		return len(self.cards)

	def discard(self, crib):
		# Currently just discards randomly
		count = 0
		while count < 2:
			index = random.randint(0, len(self.cards) - 1)
			crib.add_card(self.cards.pop(index))
			count += 1
		return

	def count_combos(self):
		pair_count = 0
		for i in range(4, 1, -1):
			combos = itertools.combinations(self.cards, i)
			for c in combos:
				if len(c) == i and all(c[0].rank == c[x].rank for x in range(1,i)):
					score_cats = {2: 'pair', 3: 'triplet', 4: 'fourkind'}
					if i == 4:
						self.score['fourkind'] = 12
						return
					elif i == 3: 
						self.score['triplet'] = 6
						return
					else:
						pair_count += 1
		self.score['pair'] = 2 * pair_count
		return

	def count_runs(self):
		#ranks = self.numerical_ranks()
		ranks = [6, 11, 12, 5]
		run_of_5 = False
		run_of_4 = False
		run_of_3 = False
				# check for runs of 4
		run_tally = 0
		for i in range(len(ranks)):
			j = i + 1
			if j == len(ranks):
				break
			else:
				if ranks[j] - ranks[i] == 1:
					run_tally += 1
				else:
					pass
		if run_tally == 4:
			run_of_5 = True
		if run_tally == 3:
			run_of_4 = True
		if run_tally == 2:
			run_of_3 = True

		print('Run of 5: {}'.format(run_of_5))
		print('Run of 4: {}'.format(run_of_4))
		print('Run of 3: {}'.format(run_of_3))
		print(run_tally)

		return run_tally


	def count_flush(self):
		suits = [c[1] for c in self.cards]
		c = Counter(suits).most_common(4)
		for i in c:
			if i[1] == 4 or i[1] == 5:
				self.score['flush'] = 4
				return True
			else:
				self.score['flush'] = 0
		return False

	def total_hand_value(self):
		return sum(c.value() for c in self.cards)

	def score_hand(self):
		return


if __name__ == '__main__':
	d = Deck()
	print('Deck created. Shuffling.')
	d.shuffle()
	print('Done. Dealing two hands.')
	p1, p2 = Hand(), Hand()

	
	d.deal(p1, p2)
	print('P1: {} Score: {}'.format(p1.cards, p1.total_hand_value()))
	print('P2: {} Score: {}'.format(p2.cards, p2.total_hand_value()))
	print('Discarding')
	print('Cutting and showing cut card.')
	d.cut()
	cut_card = d.cards[0]
	print('Cut card: {}'.format(cut_card))
	crib = Hand()
	p1.discard(crib)
	p2.discard(crib)
	print('P1: {} Score: {}'.format(p1.cards, p1.total_hand_value()))
	print('P2: {} Score: {}'.format(p2.cards, p2.total_hand_value()))
	print('Cr: {} Score: {}'.format(crib.cards, crib.total_hand_value()))
	print(' P1 Matches? {}'.format(p1.count_combos()))
	print(' P1 Matches? {}'.format(p2.count_combos()))

	p1.count_flush()
	p2.count_flush()

	print('P1 Score: {}'.format(p1.score))
	print('P2 Score: {}'.format(p2.score))

	p1.count_runs()
	print(p1.count_runs())

	
