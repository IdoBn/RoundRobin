from collections import defaultdict, Counter
from itertools import tee

from terminaltables import SingleTable
from textwrap import wrap

import argparse


class RoundRobin(object):
	"""Implements the Round Robin algorithem as explained here: https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm
	This class is an iterator and with every iteration it returns a new list of pairs. It will not return duplicate pairs.
	
	Raises:
		StopIteration -- When you have exhausted all possible pairs (without duplication) the class will raise
	"""

	def __init__(self, participants: list) -> None:
		"""Constructor of the RoundRobin class
		
		Arguments:
			participants {list} -- The list that you'd like to have all of the pairs for
		"""

		self._participants = participants
		self._rounds = len(participants) - 1

	def __iter__(self):
		return self

	def __next__(self) -> list:
		"""Returns the next list of unique pairs
		
		Raises:
			StopIteration -- Once all list of unique pairs have been exhausted this will raise
		
		Returns:
			list -- a list of tuples where every tuple contains 2 values from the given participants list
		"""


		if self._rounds == 0:
			raise StopIteration

		self._rounds -= 1
		half = self._participants[int(len(self._participants)/2):]
		res = list(zip(self._participants[:int(len(self._participants)/2)], half[::-1]))
		self._participants = [ i for i in re_arrange(self._participants, pivot=1)]
		return res


def re_arrange(arr, pivot=0):
	"""A generator to rearrange an array like so:
	[1,2,3] -> [3,1,2]
	It pushes the last value to the first value.
	
	Arguments:
		arr {[type]} -- the array you'd like to re-arrange
	
	Keyword Arguments:
		pivot {int} -- if pivot defines the place in which to place the last value of the array. (default: {0}) 
		for example if pivot is 1 then: [1,2,3] -> [1,3,2]
	"""

	def re_arrange_helper(arr):
		yield arr[-1]
		for i in arr[:-1]:
			yield i

	res = re_arrange_helper(arr[pivot:])
	for i in arr[0:pivot]:
		yield i
		
	for i in res:
		yield i


def main():
	parser = argparse.ArgumentParser(description="""A tool that is used to show all of the matches of a specific group without repetitions""")
	parser.add_argument("number", metavar='number', type=int, nargs=1,
						help="The number of participants to match up")

	args = parser.parse_args()

	length = args.number[0]
	robin = RoundRobin(range(length))

	table_data = []

	table_data.append([f"Round{i:02d}" for i in range(length-1)])
	for pairs in robin:
		for indexj, pair in enumerate(pairs):
			if len(table_data) < indexj + 2:
				table_data.append([])
			table_data[indexj+1].append(tuple(sorted(pair)))

	table = SingleTable(table_data)

	print(table.table)


if __name__ == "__main__":
    main()
