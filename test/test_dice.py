import unittest
import random

from src.dice import RollCommand, RollOperation, exec_command

class TestRollCommandMethods(unittest.TestCase):

    def test_parse_from_cmd(self):
        tests = [
            ["d8",      [RollOperation.ADD, 1, 8]],
            ["2d6",     [RollOperation.ADD, 2, 6]],
            ["-d12",    [RollOperation.SUBTRACT, 1, 12]],
            ["+12d100", [RollOperation.ADD, 12, 100]]
        ]

        for cmd, [op, num, sides] in tests:
            roll_command = RollCommand.parse(cmd)
            self.assertEqual(roll_command.operation, op)
            self.assertEqual(roll_command.num, num)
            self.assertEqual(roll_command.sides, sides)

class TestExecCommand(unittest.TestCase):

    def test_exec_command(self):
        random.seed(1)
        tests = [
            ["d8", [
                [RollOperation.ADD, 1, 8],
                [3],
                3]],
            ["2d6", [
                [RollOperation.ADD, 2, 6],
                [5, 1],
                6]],
            ["-d12", [
                [RollOperation.SUBTRACT, 1, 12],
                [-5],
                -5]],
            ["+12d100", [
                [RollOperation.ADD, 12, 100],
                [16, 64, 98, 58, 61, 84, 49, 27, 13, 63, 4, 50],
                587]]]

        for cmd, [[op, num, sides], values, sum] in tests:
            roll_command = RollCommand.parse(cmd)
            result = exec_command(roll_command)
            command = result.command
            self.assertEqual(command.operation, op)
            self.assertEqual(command.num, num)
            self.assertEqual(command.sides, sides)
            self.assertEqual(result.values, values)
            self.assertEqual(result.sum, sum)