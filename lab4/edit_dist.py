import numpy as np


def levenshtein_swap_weight(char1, char2):
    return 1 if char1 != char2 else 0


def lcs_swap_weight(char1, char2):
    return 2 if char1 != char2 else 0


def get_edit_matrix(elements1, elements2, swap_weight_func=levenshtein_swap_weight):
    size1 = len(elements1) + 1
    size2 = len(elements2) + 1
    edit_matrix = np.empty((size1, size2), dtype=np.uintc)
    edit_matrix[0, :] = np.arange(0, size2)
    edit_matrix[:, 0] = np.arange(0, size1)
    for i in range(1, size1):
        for j in range(1, size2):
            swap_weight = swap_weight_func(elements1[i - 1], elements2[j - 1])
            neigh_min = min(edit_matrix[i - 1, j - 1] + swap_weight,  # edit
                            edit_matrix[i - 1, j] + 1,  # delete
                            edit_matrix[i, j - 1] + 1)  # add
            edit_matrix[i, j] = neigh_min
    return edit_matrix


def get_di_dj(edit_matrix, i, j):
    di, dj = 1, 1
    curr_min = edit_matrix[i - 1, j - 1]
    if curr_min > edit_matrix[i, j - 1]:
        curr_min = edit_matrix[i, j - 1]
        di, dj = 0, 1
    if curr_min > edit_matrix[i - 1, j]:
        di, dj = 1, 0
    return di, dj


def get_steps(edit_matrix, i=None, j=None):
    if i is None:
        i = np.size(edit_matrix, 0) - 1
    if j is None:
        j = np.size(edit_matrix, 1) - 1
    steps = []
    while (i, j) != (0, 0):
        di, dj = 0, 0
        if i == 0:
            dj = 1
        elif j == 0:
            di = 1
        else:
            di, dj = get_di_dj(edit_matrix, i, j)
        i -= di
        j -= dj
        steps.insert(0, (di, dj))
    return steps


def get_edits(edit_matrix, str1, str2):
    steps = get_steps(edit_matrix)

    prev_word = list(str1)
    output = [str1, " -> ", str2, "\n"]
    i, j, certain = 0, 0, 0
    for di, dj in steps:
        if (di, dj) == (1, 0):
            del prev_word[certain]
        elif (di, dj) == (0, 1):
            prev_word.insert(certain, str2[j])
            certain += 1
        else:
            prev_word[certain] = str2[j]
            certain += 1
            if str1[i] == str2[j]:
                i += di
                j += dj
                continue
        i += di
        j += dj
        output.append("".join(prev_word))
        output.append("\n")
    del output[-1]  # delete last \n
    return "".join(output)


# print_steps only works for strings
def edit_dist(elements1, elements2, swap_weigh_func=levenshtein_swap_weight, print_steps=False):
    edit_matrix = get_edit_matrix(elements1, elements2, swap_weigh_func)
    if print_steps:
        if not (type(elements1) == type(elements2) == str):
            raise(Exception("Printing steps only available for strings"))
        print(get_edits(edit_matrix, elements1, elements2))
    return edit_matrix[len(elements1), len(elements2)]


def main():
    str1 = "abcdef"
    str2 = "acbcf"
    edit_m = get_edit_matrix(str1, str2, swap_weight_func=lcs_swap_weight)
    print(edit_m)
    print(get_steps(edit_m))

    dist = edit_dist(str1, str2, print_steps=True)
    print(dist)


if __name__ == '__main__':
    main()
