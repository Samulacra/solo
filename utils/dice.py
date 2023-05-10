import random
import re

class Die():
    def __init__(self, sides) -> None:
        self._sides = sides

    def __str__(self) -> str:
        return "d" + str(self._sides)
    
    @property
    def sides(self) -> int:
        return self._sides

    def roll(self, r: random.Random = random) -> int:
        return r.randint(1, self._sides)

d2 = Die(2)
d3 = Die(3)
d4 = Die(4)    
d6 = Die(6)
d8 = Die(8)
d10 = Die(10)
d12 = Die(12)
d20 = Die(20)
d100 = Die(100)

class PartialResult():
    def __init__(self, command: str, values: list[int], value: int) -> None:
        self._command = command
        self._values = values
        self._value = value
    
    @property
    def command(self) -> str:
        return self._command
    
    @property
    def values(self) -> list[int]:
        return self._values
    
    @property
    def value(self) -> int:
        return self._value

class Result():
    def __init__(self, command: str, partials: list[PartialResult], value: int) -> None:
        self._command = command
        self._partials = partials
        self._value = value

    @property
    def command(self) -> str:
        return self._command
    
    @property
    def partials(self) -> list[PartialResult]:
        return self._partials
    
    @property
    def value(self) -> int:
        return self._value

_split_pattern = re.compile("([+-])?(\d+)?(d)?(\d+)")

def _split_command(command: str):
    out: list[tuple[str, tuple[str, ...]]] = []
    idx = 0
    match = _split_pattern.search(command, idx)
    while match is not None:
        _, end = match.span()
        out.append((match.group(), match.groups()))
        idx = end
        match = _split_pattern.search(command, idx)
    if idx != len(command):
        raise "Split failed, invalid command"
    return out

def _exec_part(part: tuple[str, tuple[str, ...]], r: random.Random) -> PartialResult:
    (cmd, (op, num_times, is_die, value)) = part
    op = (lambda x: x) if op != "-" else (lambda x: -x)
    value = int(float(value))
    if is_die:
        num_times = int(float(num_times or "1"))
        values = [op(r.randint(1, value)) for _ in range(num_times)]
        value = sum(values)
    else:
        value = op(value)
        values = [value]
    return PartialResult(cmd, values, value)

def roll(command: str, r: random.Random = random) -> Result:
    parts = _split_command(command)
    partial_results = [_exec_part(part, r) for part in parts]
    return Result(
        command,
        partial_results,
        sum([partial.value for partial in partial_results]))