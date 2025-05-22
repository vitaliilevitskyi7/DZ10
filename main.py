from math import gcd
from typing import Union

class Rational:
    def __init__(self, n: Union[int, str], d: int = 1):
        if isinstance(n, str):
            n, d = map(int, n.split("/"))
        if d == 0:
            raise ValueError("Denominator cannot be zero")
        g = gcd(n, d)
        self._n = n // g
        self._d = d // g
        if self._d < 0:
            self._n *= -1
            self._d *= -1

    def __add__(self, other):
        other = Rational(other) if isinstance(other, int) else other
        return Rational(self._n * other._d + other._n * self._d, self._d * other._d)

    def __str__(self):
        return f"{self._n}/{self._d}"

    def __call__(self):
        return self._n / self._d


class RationalList:
    def __init__(self):
        self.items = []

    def __getitem__(self, index):
        return self.items[index]

    def __setitem__(self, index, value):
        if isinstance(value, int):
            value = Rational(value)
        elif not isinstance(value, Rational):
            raise TypeError("Only Rational or int allowed")
        self.items[index] = value

    def __len__(self):
        return len(self.items)

    def __add__(self, other):
        result = RationalList()
        result.items = self.items[:]
        if isinstance(other, RationalList):
            result.items.extend(other.items)
        elif isinstance(other, (Rational, int)):
            result.items.append(Rational(other))
        else:
            raise TypeError("Unsupported type")
        return result

    def __iadd__(self, other):
        if isinstance(other, RationalList):
            self.items.extend(other.items)
        elif isinstance(other, (Rational, int)):
            self.items.append(Rational(other))
        else:
            raise TypeError("Unsupported type")
        return self

    def append(self, value):
        if isinstance(value, int):
            value = Rational(value)
        elif not isinstance(value, Rational):
            raise TypeError("Only Rational or int allowed")
        self.items.append(value)

    def sum(self):
        total = Rational(0)
        for r in self.items:
            total += r
        return total


def parse_file(filename):
    rlist = RationalList()
    with open(filename, "r") as f:
        for line in f:
            tokens = line.strip().split()
            for tok in tokens:
                rlist.append(Rational(tok) if '/' in tok else Rational(int(tok)))
    return rlist


def main():
    files = ["input01.txt", "input02.txt", "input03.txt"]
    with open("output_demo.txt", "w") as out:
        for fname in files:
            rlist = parse_file(fname)
            total = rlist.sum()
            out.write(f"{fname}: {total} = {total():.5f}\n")

if __name__ == "__main__":
    main()