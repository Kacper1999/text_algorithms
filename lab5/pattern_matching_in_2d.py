from lab5.aho_corasick import Automaton
from lab5.pattern_matching_in_1d import kmp_pattern_matching
from typing import List
import os

Los = List[str]  # List Of Strings

# https://en.wikipedia.org/wiki/Private_Use_Areas pretty nice
marker = chr(0xF0000)


class Column:
    def __init__(self, i):
        self.sequences = []
        self.starts = []
        self.i = i

    def add_seq(self, seq, start):
        self.sequences.append(seq)
        self.starts.append(start)

    def find(self, pattern):
        output = []
        p_len = len(pattern)
        for seq, start in zip(self.sequences, self.starts):
            output += [(s + start + p_len - 1, self.i) for s in kmp_pattern_matching(seq, pattern)]
        return output

    def __str__(self, indent="\t"):
        output = []
        for text, start in zip(self.sequences, self.starts):
            output.append(f"{indent}{text} starting at: {start}\n")
        return "".join(output)


def get_columns(rows: Los, max_row_len):
    rows_num = len(rows)
    cols = []
    for i in range(max_row_len):
        curr_seq = []
        col = Column(i)
        start = 0
        for j in range(rows_num):
            try:
                curr_seq.append(rows[j][i])
            except IndexError:
                if curr_seq:
                    col.add_seq(curr_seq, start)
                start = j + 1
                curr_seq = []
        if curr_seq:
            col.add_seq(curr_seq, start)
        cols.append(col)
    return cols


def file_to_los(file_path: str):
    table = []
    with open(file_path) as f:
        for i, row in enumerate(f):
            if row[-1] == "\n":
                row = row[:-1]
            table.append(row)
    return table


# List Of Lists to List Of Strings
def lol_to_los(lol):
    return ["".join([str(x) for x in row]) for row in lol]


# works only for rectangular pattern
def lol_2d_match(lol, pattern):
    return los_2d_match(lol_to_los(lol), lol_to_los(pattern))


def f_2d_match(file_path: str, pattern: Los):
    text = file_to_los(file_path)
    return los_2d_match(text, pattern)


def los_2d_match(text: Los, pattern: Los, automaton=None):
    if automaton is None:
        automaton = Automaton(set(row for row in pattern))
    max_row_len = 0
    for row in text:
        max_row_len = max(max_row_len, len(row))

    states = [automaton.get(row)[1] for row in text]
    to_find = [automaton.get_last_state(row) for row in pattern]
    columns = get_columns(states, max_row_len)
    output = []
    for col in columns:
        output += col.find(to_find)
    return output


def main():
    file_name = "haystack.txt"
    test_dir = "test_files"
    file_path = os.path.join(os.getcwd(), test_dir, file_name)
    a = f_2d_match(file_path, ["t h", "t h"])

    pattern = ["T h e search of words or p a t t e r n s in stat",
               "t h a n the previous pattern-matching mechanism."]
    b = f_2d_match(file_path, pattern)
    c = los_2d_match(["t h", "t h"], ["t h", "t h"])
    d = lol_2d_match([["t", " ", "h"], ["t", " ", "h"]], [["t", " ", "h"], ["t", " ", "h"]])

    print(d)
    print(c)
    print(b)
    print(a)


if __name__ == '__main__':
    main()
