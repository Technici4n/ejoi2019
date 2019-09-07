#!/usr/bin/python3 -sS

import io
import sys


class Solver:
    """
    Solves the output
    """
    def __init__(self):
        self._current = [1]
        self._prefix_sums = [0, 1]

    def update(self, l: int, u: int) -> None:
        if l < 1 or u > len(self._current) or l > u:
            print("0.0")
            print("Output malformed", file=sys.stderr)
            raise
        range_sum = self._prefix_sums[u] - self._prefix_sums[l - 1]
        self._current.append(range_sum)
        self._prefix_sums.append(self._prefix_sums[-1] + self._current[-1])

    def check_result(self, final_value: int):
        if self._current[-1] == final_value:
            return len(self._current) - 1
        return -1


class Checker:
    """
    This class checks the whole subtask and returns the result
    """
    def __init__(self, input_file: str, solution: str, output:str):
        """
        :param solution: path to the solution file
        :param output: path to the output file
        """

        self._output_file = output
        #
        with io.open(input_file, 'r') as f:
            ints = [int(s.strip()) for s in f.readlines()]
            self.qs = ints[1:]

        with io.open(solution, 'r') as f:
            arr = [[int(x) for x in i.split()] for i in f.readlines()]

        self._jury_length = []
        for e in arr:
            if len(e) == 1:
                self._jury_length.append(e[0])
        self._solver = None
        self._contestant_length = list()

    def check_contestant_length(self):
        """
        Checks the solution
        """
        with io.open(self._output_file, 'rb') as output:
            for q in self.qs:
                self._solver = Solver()
                n = int(output.readline().strip())

                for i in range(n):
                    try:
                        ss = output.readline().strip().split()
                        l, r = [int(token) for token in ss]
                        self._solver.update(l, r)
                    except ValueError:
                        raise Exception("Output malformed")

                result = self._solver.check_result(q)
                if result == -1:
                    raise Exception("Not valid tower")
                self._contestant_length.append(n)

    def get_score(self):
        """
        Scores and prints the result
        """
        if len(self._jury_length) != len(self._contestant_length):
            print("0.0")
            print("Output malformed", file=sys.stderr)
            return
        if self._jury_length == self._contestant_length:
            print("1.0")
            print("Correct", file=sys.stderr)
            return
        # print(list(zip(self._jury_length, self._contestant_length)))
        scores = []
        for i, j in zip(self._jury_length, self._contestant_length):
            if j != 0:
                scores.append(i * 0.7 / j + 0.1)
            else:
                scores.append(0.8)
        print("%.2f" % min(scores))
        print("Correct", file=sys.stderr)
        return


# Read file paths from args
input_file, solution_file, output_file = sys.argv[1:]
checker = Checker(input_file, solution_file, output_file)

# Ensure output is of the form "<word> <number>" where word is from the
# solution, and number is from the student.
try:
    checker.check_contestant_length()
    checker.get_score()
except Exception as err:
    print("0.0")
    print(str(err), file=sys.stderr)
