import copy
import time
from functools import reduce
from operator import mul
from unittest import TestCase

from dice import Dice

tiny_grid = [
	[6, 2],
	[3, 4],
]

tiny_grid_with_hole = [
	[6, 2],
	[0, 4],
]

small_grid = [
	[3, 4, 1, 7, 5],
	[1, 2, 4, 3, 5],
	[2, 4, 3, 6, 2],
	[9, 5, 7, 2, 3],
	[5, 8, 3, 4, 1],
]

full_grid = [
	[1, 5, 4, 4, 6, 1, 1, 4, 1, 3, 7, 5],
	[3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[4, 0, 6, 4, 1, 8, 1, 4, 2, 1, 0, 3],
	[7, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 2],
	[1, 0, 1, 0, 6, 1, 6, 2, 0, 2, 0, 1],
	[8, 0, 4, 0, 1, 0, 0, 8, 0, 3, 0, 5],
	[4, 0, 2, 0, 5, 0, 0, 3, 0, 5, 0, 2],
	[8, 0, 5, 0, 1, 1, 2, 3, 0, 4, 0, 6],
	[6, 0, 1, 0, 0, 0, 0, 0, 0, 3, 0, 6],
	[3, 0, 6, 3, 6, 5, 4, 3, 4, 5, 0, 1],
	[6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
	[2, 1, 6, 6, 4, 5, 2, 1, 1, 1, 7, 1],
]

empty_line = [[0, 0, 0]]

stripped_grid = [row[2:-2] for row in full_grid[2:-2]]

max_dice = None
max_grid = None
max_visited = None


def max_score(grid):
	dice = Dice()
	visited = [[False for j in grid[i]] for i in range(len(grid))]
	x, y = 0, 0
	product = 1
	success_products = []

	max_score_recursive(grid, visited, dice, x, y, product, success_products)

	return max(success_products)


def max_score_recursive(grid, visited, dice, x, y, product, success_products):
	global max_dice
	global max_grid
	global max_visited

	grid_modified = False
	dice_modified = False

	if dice.get_value() == 0 and grid[x][y] != 0:
		dice.set_value(grid[x][y])
		dice_modified = True
	elif dice.get_value() != 0 and grid[x][y] == 0:
		grid[x][y] = dice.get_value()
		grid_modified = True
	elif dice.get_value() == 0 and grid[x][y] == 0:
		for i in range(1, 10):
			grid[x][y] = i
			max_score_recursive(grid, visited, dice, x, y, product, success_products)
		grid[x][y] = 0
		return
	elif grid[x][y] != dice.get_value():
		return

	product *= grid[x][y]

	if x == len(grid) - 1 and y == len(grid[0]) - 1:
		if product > max(success_products or [0]):
			max_dice = copy.deepcopy(dice)
			max_grid = copy.deepcopy(grid)
			max_visited = copy.deepcopy(visited)
		success_products.append(product)
	else:
		visited[x][y] = True

		if x < len(grid) - 1 and not visited[x + 1][y]:
			dice.tip_south()
			max_score_recursive(grid, visited, dice, x + 1, y, product, success_products)
			dice.tip_north()
		if x > 0 and not visited[x - 1][y]:
			dice.tip_north()
			max_score_recursive(grid, visited, dice, x - 1, y, product, success_products)
			dice.tip_south()
		if y < len(grid[0]) - 1 and not visited[x][y + 1]:
			dice.tip_east()
			max_score_recursive(grid, visited, dice, x, y + 1, product, success_products)
			dice.tip_west()
		if y > 0 and not visited[x][y - 1]:
			dice.tip_west()
			max_score_recursive(grid, visited, dice, x, y - 1, product, success_products)
			dice.tip_east()

	# Undo stuff to avoid copying
	visited[x][y] = False
	if grid_modified:
		grid[x][y] = 0
	if dice_modified:
		dice.set_value(0)


class TestTravelAgent(TestCase):
	def test_tiny_grid(self):
		self.assertEqual(6 * 3 * 4, max_score(tiny_grid))

	def test_small_grid(self):
		self.assertEqual(276480, max_score(small_grid))

	def test_tiny_grid_with_holes(self):
		self.assertEqual(6 * 9 * 4, max_score(tiny_grid_with_hole))

	def test_stripped_grid(self):
		self.assertEqual(1337415067238400000000, max_score(stripped_grid))

	def test_empty_line(self):
		self.assertEqual(9 * 9 * 9, max_score(empty_line))


def main():
	start_time = time.time()
	print(max_score(stripped_grid))
	#print(max_score(full_grid))
	print(max_dice.faces)
	print(max_grid)
	print(max_visited)
	print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
	main()
