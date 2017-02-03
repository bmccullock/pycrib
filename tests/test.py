import unittest
from crib2 import Card, Deck, Hand, Game

class HandTests(unittest.TestCase):

	def setUp(self):
		self.h = Hand()
		self.h.cards = [
			Card(1, 'H'),
			Card(1, 'C'),
			Card(3, 'D'),
			Card(4, 'S'),
			Card(5, 'C'),
		]
		self.crib = Hand()

	def test_discard(self):
		hand_cnt = len(self.h)
		crib_cnt = len(self.crib)
		self.h.discard(self.crib)

		self.assertEquals(len(self.h), hand_cnt - 2)
		self.assertEquals(len(self.crib), crib_cnt + 2)

class PairsTests(unittest.TestCase):

	def setUp(self):
		self.h = Hand()

	def test_is_pair(self):
		self.h.cards = [
			Card(1, 'H'),
			Card(1, 'H'),
			Card(3, 'H'),
			Card(4, 'H'),
			Card(5, 'H'),
		]
		pairs = self.h.pairs()
		self.assertEquals(pairs[0][0], pairs[0][1])

	def test_no_pairs(self):
		self.h.cards = [
			Card(1, 'H'),
			Card(2, 'H'),
			Card(3, 'H'),
			Card(4, 'H'),
			Card(5, 'H'),
		]
		self.assertEquals(len(self.h.pairs()), 0)

	def test_two_pairs(self):
		self.h.cards = [
			Card(1, 'H'),
			Card(1, 'H'),
			Card(3, 'H'),
			Card(3, 'H'),
			Card(5, 'H'),
		]
		self.assertEquals(len(self.h.pairs()), 2)

	def test_triplet(self):
		self.h.cards = [
			Card(1, 'H'),
			Card(1, 'H'),
			Card(1, 'H'),
			Card(4, 'H'),
			Card(5, 'H'),
		]
		self.assertEquals(len(self.h.pairs()), 3)

	def test_four_kind(self):
		self.h.cards = [
			Card(1, 'H'),
			Card(1, 'H'),
			Card(1, 'H'),
			Card(1, 'H'),
			Card(5, 'H'),
		]
		self.assertEquals(len(self.h.pairs()), 6)

class FifteensTests(unittest.TestCase):

	def setUp(self):
		self.h = Hand()

	def test_no_fifteens(self):
		self.h.cards = [
			Card(1, 'H'),
			Card(1, 'H'),
			Card(1, 'H'),
			Card(1, 'H'),
			Card(1, 'H'),
		]

		self.assertEquals(len(self.h.fifteens()), 0)
	
	def test_one_fifteens(self):
		self.h.cards = [
			Card(1, 'H'),
			Card(1, 'H'),
			Card(1, 'H'),
			Card(8, 'H'),
			Card(7, 'H'),
		]

		self.assertEqual(len(self.h.fifteens()), 1)

	def test_valid_fifteens(self):
		self.h.cards = [
			Card(1, 'H'),
			Card(1, 'H'),
			Card(1, 'H'),
			Card(1, 'H'),
			Card(2, 'H'),
		]

		fifteens = self.h.fifteens()
		for c in fifteens:
			self.assertEqual(c[0] + c[1], 15)


class FlushTests(unittest.TestCase):

	def setUp(self):
		self.h = Hand()

	def test_no_flush(self):
		self.h.cards = [
			Card(1, 'H'),
			Card(1, 'C'),
			Card(3, 'D'),
			Card(4, 'S'),
			Card(5, 'C'),
		]
		self.assertFalse(self.h.flush())

	def test_is_flush(self):
		self.h.cards = [
			Card(1, 'H'),
			Card(1, 'H'),
			Card(3, 'H'),
			Card(4, 'H'),


			Card(5, 'H'),
		]
		self.assertTrue(self.h.flush())

class RunTests(unittest.TestCase):

	def setUp(self):
		self.h = Hand()

	def test_no_run(self):
		self.h.cards = [
			Card(1, 'H'),
			Card(3, 'C'),
			Card(5, 'D'),
			Card(7, 'S'),
			Card(9, 'C'),
		]
		self.assertFalse(self.h.runs())

	def test_run_three(self):
		self.h.cards = [
			Card(1, 'H'),
			Card(1, 'C'),
			Card(3, 'D'),
			Card(4, 'S'),
			Card(5, 'C'),
		]
		self.assertEquals(self.h.runs(), [[3, 4, 5]])

	def test_run_four(self):
		self.h.cards = [
			Card(1, 'H'),
			Card(2, 'C'),
			Card(3, 'D'),
			Card(4, 'S'),
			Card(9, 'C'),
		]
		self.assertEquals(self.h.runs(), [[1,2, 3, 4]])

	def test_run_five(self):
		self.h.cards = [
			Card(1, 'H'),
			Card(2, 'C'),
			Card(3, 'D'),
			Card(4, 'S'),
			Card(5, 'C'),
		]
		self.assertEquals(self.h.runs(), [[1, 2, 3, 4, 5]])	

	def test_run_three_one_dup(self):
		self.h.cards = [
			Card(1, 'H'),
			Card(3, 'C'),
			Card(3, 'D'),
			Card(4, 'S'),
			Card(5, 'C'),
		]
		self.assertEquals(self.h.runs(), [[3, 4, 5], [3, 4, 5]])

	def test_run_three_two_dup(self):
		self.h.cards = [
			Card(3, 'H'),
			Card(3, 'C'),
			Card(3, 'D'),
			Card(4, 'S'),
			Card(5, 'C'),
		]
		self.assertEquals(self.h.runs(), [[3, 4, 5], [3, 4, 5], [3, 4, 5]])

	def test_run_four_one_dup(self):
		self.h.cards = [
			Card(2, 'H'),
			Card(2, 'C'),
			Card(3, 'D'),
			Card(4, 'S'),
			Card(5, 'C'),
		]
		self.assertEquals(self.h.runs(), [[2, 3, 4, 5], [2, 3, 4, 5]])

class HisNobsTests(unittest.TestCase):
	""""""

	def setUp(self):
		self.h = Hand()
		self.starter = Card(1, 'S')

	def test_no_nobs(self):
		self.h.cards = [
			Card(1, 'H'),
			Card(1, 'H'),
			Card(3, 'H'),
			Card(4, 'H'),
			Card(5, 'H'),
		]
		self.assertFalse(self.h.his_nobs(self.starter))

	def test_yes_nobs(self):
		self.h.cards = [
			Card(1, 'H'),
			Card(1, 'H'),
			Card(3, 'H'),
			Card(4, 'H'),
			Card(11, 'S'),
		]
		self.assertTrue(self.h.his_nobs(self.starter))

if __name__ == '__main__':
	unittest.main()