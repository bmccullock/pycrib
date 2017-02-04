from collections import namedtuple, Counter
import itertools
import random

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
	"""A small Deck. Implements some methods for accessing cards as suits and
	 values."""
	def __init__(self):
		super(Hand, self).__init__()
		self.cards = []

	def __str__(self):
		return ' '.join(map(str, self.cards))

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

	__repr__ = __str__
		