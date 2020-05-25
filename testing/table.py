import pandas as pd
import numpy as np

file_path = "segments.csv"

def get_pos(n):
    if n == 2:
        return 3
    if n == 3:
        return 2
    return n

def get_table(data, char):
    col = data[char]
    dim = 4
    table = np.zeros((dim, dim), dtype=np.int32)
    for i, v in enumerate(col):
        table[get_pos(i // dim), get_pos(i % dim)] = v
    return table


def get_tables(data):
    output = []
    for char in data.columns.values[1:]:
        output.append(get_table(data, char))
    return output


def print_tables(data):
    for char in data.columns.values[1:]:
        print("input", char)
        print(get_table(data, char))
        print("------")

def i_j_to_char(i, j):
    pass

def get_bool_f(table):
    for i, row in enumerate(table):
        for j, state in enumerate(row):
            char = i_j_to_char(i, j)


def main():
    data = pd.read_csv(file_path)
    tables = get_tables(data)
    print_tables(data)


if __name__ == '__main__':
    main()
