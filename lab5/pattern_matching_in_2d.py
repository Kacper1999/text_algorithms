from lab5.aho_corasick import Automaton
from typing import List
import re
import os

Los = List[str]  # List Of Strings

# https://en.wikipedia.org/wiki/Private_Use_Areas pretty nice
marker = chr(0xF0000)


class Column:
    def __init__(self, i):
        self.texts: Los = []
        self.starts = []
        self.i = i

    def add_text(self, text, start):
        self.texts.append(text)
        self.starts.append(start)

    def find(self, pattern):
        output = []
        p_len = len(pattern)
        for text, start in zip(self.texts, self.starts):
            output += [(m.start() + start + p_len - 1, self.i) for m in re.finditer(f'(?={pattern})', text)]
        return output

    def __str__(self, indent="\t"):
        output = []
        for text, start in zip(self.texts, self.starts):
            output.append(f"{indent}{text} starting at: {start}\n")
        return "".join(output)


def get_columns(rows: Los, max_row_len):
    rows_num = len(rows)
    cols = []
    for i in range(max_row_len):
        curr_text = []
        col = Column(i)
        start = 0
        for j in range(rows_num):
            try:
                curr_text.append(rows[j][i])
            except IndexError:
                if curr_text:
                    col.add_text("".join(curr_text), start)
                start = j + 1
                curr_text = []
        if curr_text:
            col.add_text("".join(curr_text), start)
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
    return str_2d_match(lol_to_los(lol), lol_to_los(pattern))


def f_2d_match(file_path: str, pattern: Los):
    text = file_to_los(file_path)
    return str_2d_match(text, pattern)


def str_2d_match(text: Los, pattern: Los):
    max_row_len = 0
    for row in text:
        max_row_len = max(max_row_len, len(row))
    patterns = set(row for row in pattern)
    automaton = Automaton(patterns)

    states = ["".join([str(state) for state in automaton.get(row)[1]]) for row in text]
    columns = get_columns(states, max_row_len)
    to_find = "".join([str(automaton.get_last_state(row)) for row in pattern])
    output = []

    for i, col in enumerate(columns):
        output += col.find(to_find)
    return output


def main():
    file_name = "haystack.txt"
    test_dir = "test_files"
    file_path = os.path.join(os.getcwd(), test_dir, file_name)
    a = f_2d_match(file_path, ["t h", "t h"])

    lol = [[(0, 0, 0), (0, 0, 0)], [(25, 25, 25), (25, 25, 25)]]
    print(lol_to_los(lol))
    # print(a)


if __name__ == '__main__':
    main()
