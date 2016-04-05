from unittest import TestCase


class Dice(object):
	def __init__(self):
		self.faces = [0] * 6
		self.up_index = 0
		self.down_index = 5
		self.north_index = 1
		self.south_index = 4
		self.west_index = 2
		self.east_index = 3

	def tip_west(self):
		old_west = self.west_index
		self.west_index = self.up_index
		self.up_index = self.east_index
		self.east_index = self.down_index
		self.down_index = old_west

	def tip_east(self):
		old_east = self.east_index
		self.east_index = self.up_index
		self.up_index = self.west_index
		self.west_index = self.down_index
		self.down_index = old_east

	def tip_north(self):
		old_north = self.north_index
		self.north_index = self.up_index
		self.up_index = self.south_index
		self.south_index = self.down_index
		self.down_index = old_north

	def tip_south(self):
		old_south = self.south_index
		self.south_index = self.up_index
		self.up_index = self.north_index
		self.north_index = self.down_index
		self.down_index = old_south

	def get_value(self):
		return self.faces[self.up_index]

	def set_value(self, value):
		self.faces[self.up_index] = value


class TestDice(TestCase):
	def setUp(self):
		self.dice = Dice()

	def _dice_valid(self):
		if (
								self.dice.up_index + self.dice.down_index == 5 and
								self.dice.north_index + self.dice.south_index == 5 and
							self.dice.west_index + self.dice.east_index == 5
		):
			return True
		return False

	def test_tip_west(self):
		self.dice.tip_west()

		self.assertTrue(self._dice_valid())
		self.assertEqual(self.dice.up_index, 3)
		self.assertEqual(self.dice.down_index, 2)
		self.assertEqual(self.dice.north_index, 1)
		self.assertEqual(self.dice.south_index, 4)
		self.assertEqual(self.dice.west_index, 0)
		self.assertEqual(self.dice.east_index, 5)

	def test_tip_east(self):
		self.dice.tip_east()

		self.assertTrue(self._dice_valid())
		self.assertEqual(self.dice.up_index, 2)
		self.assertEqual(self.dice.down_index, 3)
		self.assertEqual(self.dice.north_index, 1)
		self.assertEqual(self.dice.south_index, 4)
		self.assertEqual(self.dice.west_index, 5)
		self.assertEqual(self.dice.east_index, 0)

	def test_tip_north(self):
		self.dice.tip_north()

		self.assertTrue(self._dice_valid())
		self.assertEqual(self.dice.up_index, 4)
		self.assertEqual(self.dice.down_index, 1)
		self.assertEqual(self.dice.north_index, 0)
		self.assertEqual(self.dice.south_index, 5)
		self.assertEqual(self.dice.west_index, 2)
		self.assertEqual(self.dice.east_index, 3)

	def test_tip_south(self):
		self.dice.tip_south()

		self.assertTrue(self._dice_valid())
		self.assertEqual(self.dice.up_index, 1)
		self.assertEqual(self.dice.down_index, 4)
		self.assertEqual(self.dice.north_index, 5)
		self.assertEqual(self.dice.south_index, 0)
		self.assertEqual(self.dice.west_index, 2)
		self.assertEqual(self.dice.east_index, 3)
