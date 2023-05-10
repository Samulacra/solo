import unittest
import random

from utils import dice

class TestDie(unittest.TestCase):

    def test_default_die(self):
        random.seed(int("deadbeef", 16))

        tests: list[list[dice.Die, list[str, int]]] = [
            (dice.d2,   ("d2", 1)),
            (dice.d3,   ("d3", 2)),
            (dice.d4,   ("d4", 4)),
            (dice.d6,   ("d6", 5)),
            (dice.d8,   ("d8", 7)),
            (dice.d10,  ("d10", 10)),
            (dice.d12,  ("d12", 7)),
            (dice.d20,  ("d20", 15)),
            (dice.d100, ("d100", 43))]

        for (die, (die_name, roll_value)) in tests:
            self.assertEqual(str(die), die_name)
            self.assertEqual(die.roll(), roll_value)

    def test_die_constructor(self):
        random.seed(int("deadbeef", 16))
        die = dice.Die(666)
        self.assertEqual(str(die), "d666")
        self.assertEqual(die.roll(), 20)

class TestRoll(unittest.TestCase):

    def test_split_command(self):
        tests = [
            ("4",              [("4",     (None, None, None, "4"))]),
            ("+4",             [("+4",    ("+", None, None, "4"))]),
            ("d3",             [("d3",    (None, None, "d", "3"))]),
            ("+d3",            [("+d3",   ("+", None, "d", "3"))]),
            ("2d12",           [("2d12",  (None, "2", "d", "12"))]),
            ("2d12+4-d8+12d6", [("2d12",  (None, "2", "d", "12")),
                                ("+4",    ("+", None, None, "4")),
                                ("-d8",   ("-", None, "d", "8")),
                                ("+12d6", ("+", "12", "d", "6"))])]
        for (command, expected) in tests:
            parts = dice._split_command(command)
            self.assertEqual(parts, expected)

    def test_exec_part(self):
        random.seed(int("deadbea7", 16))

        tests = [
            ("4",    (4,  [4])),
            ("+4",   (4,  [4])),
            ("-4",   (-4, [-4])),
            ("d4",   (1,  [1])),
            ("1d4",  (4,  [4])),
            ("+d4",  (1,  [1])),
            ("+1d4", (2,  [2])),
            ("-d4",  (-4, [-4])),
            ("-1d4", (-2, [-2])),
            ("-d4",  (-4, [-4])),
            ("-1d4", (-1, [-1])),
            ("2d20", (24,  [9, 15]))
        ]

        for (command, (value, values)) in tests:
            part = dice._split_command(command)[0]
            partial_result = dice._exec_part(part, random)
            
            self.assertEqual(partial_result.command, command)
            self.assertEqual(partial_result.value, value)
            self.assertEqual(partial_result.values, values)

    def test_roll(self):
        random.seed(int("deadbeef", 16))

        tests = [("2d20+d4-2", 17, [("2d20", 15, [1, 14]),
                                    ("+d4", 4, [4]),
                                    ("-2", -2, [-2])])]

        for (command, value, partials) in tests:
            result = dice.roll(command)
            self.assertEqual(result.command, command)
            self.assertEqual(result.value, value) 
            self.assertEqual(
                [(partial.command, partial.value, partial.values) for partial in result.partials],
                partials)