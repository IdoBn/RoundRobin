import unittest
from round_robin import RoundRobin, re_arrange
from collections import Counter

class TestRoundRobin(unittest.TestCase):

    def test_re_arrange(self):
        def un_generate(generator):
            return [i for i in generator]

        self.assertEqual(un_generate(re_arrange([1,2,3])), [3,1,2])
        self.assertEqual(un_generate(re_arrange([1,2,3], pivot=1)), [1,3,2])
        self.assertEqual(un_generate(re_arrange([1,2,3,4,5,6], pivot=3)), [1,2,3,6,4,5])

    def test_round_robin(self):
        robin = RoundRobin(range(1,15))
        for index, pairs in enumerate(robin):
            if 0 == index or index == 13:
                self.assertEqual(sorted(pairs), sorted([
                    (1,14),
                    (2,13),
                    (3, 12),
                    (4, 11),
                    (5, 10),
                    (6, 9),
                    (7, 8)
                ]))
            elif 2 == index:
                self.assertEqual(sorted(pairs), sorted([
                    (1,12),
                    (13,11),
                    (14, 10),
                    (2, 9),
                    (3, 8),
                    (4, 7),
                    (5, 6)
                ]))
            elif 12 == index:
                self.assertEqual(sorted(pairs), sorted([
                   (1,2),
                   (3,14),
                   (4,13),
                   (5,12),
                   (6,11),
                   (7,10),
                   (8,9) 
                ]))

    def test_no_duplicates(self):
        l = []

        for pairs in RoundRobin(range(0, 12)):
            for pair in pairs:
                l.append(tuple(sorted(pair)))

        [self.assertLessEqual(i, 1) for i in Counter(sorted(l)).values()]


if __name__ == '__main__':
    unittest.main()