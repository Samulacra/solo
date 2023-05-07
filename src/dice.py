import random
import re

from enum import Enum

def command_to_parts(cmd: str) -> list[str]:
    out = []

    _cmd = cmd[:]
    pattern = re.compile("[+-]*(/d)*d(/d)+")
    match = re.search(pattern, _cmd)

    while match:
        span = match.span()
        out.append(_cmd[:span[0]])
        out.append(match.group())
        _cmd = _cmd[span[1]:]
        match = re.search(pattern, _cmd)
    
    if len(_cmd) > 0:
        out.append(_cmd)

    return out

RollOperation = Enum('RollOperation', ["ADD", "SUBTRACT"])
    
roll_cmd_pattern = re.compile("([+-])?(\d+)?d(\d+)")

class RollCommand():
    def parse(cmd: str):
        match = re.match(roll_cmd_pattern, cmd)
        if match is None:
            raise "Invalid roll command"
        
        _op, _num, _sides = match.groups()

        op = RollOperation.ADD
        if _op == "-":
            op = RollOperation.SUBTRACT

        num = 1
        if _num is not None:
            num = int(float(_num))
        
        if _sides is None:
            raise "Invalid roll command"
        sides = int(float(_sides))

        return RollCommand(op, num, sides)

    def __init__(self, operation: RollOperation, num: int, sides: int) -> None:
        self._operation: RollOperation = operation
        self._num: int = num
        self._sides: int = sides
        return
    
    @property
    def operation(self) -> RollOperation:
        return self._operation
    
    @property
    def num(self) -> int:
        return self._num
    
    @property
    def sides(self) -> int:
        return self._sides
    
class RollResult():
    def __init__(self, command: RollCommand, values: list[int]) -> None:
        self._command = command
        self._values = [value for value in values]
        self._sum = sum(self._values)

    @property
    def command(self) -> RollCommand:
        return self._command

    @property
    def values(self) -> list[int]:
        return [value for value in self._values]
    
    @property
    def sum(self) -> int:
        return self._sum

def exec_command(cmd: RollCommand) -> RollResult:
    _values = map(
        (lambda val: val if cmd.operation is RollOperation.ADD else -val),
        [random.randint(1, cmd.sides) for _ in range(cmd.num)]
    )
    return RollResult(cmd, _values)