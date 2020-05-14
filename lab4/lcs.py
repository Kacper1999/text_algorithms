from lab4.edit_dist import edit_dist, lcs_swap_weight, get_steps, get_edit_matrix
from itertools import zip_longest


def get_lcs_len(elements1, elements2):
    lcs_edit_d = edit_dist(elements1, elements2, swap_weigh_func=lcs_swap_weight)
    return (len(elements1) + len(elements2) - lcs_edit_d) // 2


def get_lcs(elements1, elements2):
    edit_m = get_edit_matrix(elements1, elements2, swap_weight_func=lcs_swap_weight)
    steps = get_steps(edit_m)
    i, j = 0, 0
    lcs = []
    for di, dj in steps:
        if (di, dj) == (1, 1) and elements1[i] == elements2[j]:
            lcs.append(elements1[i])
        i += di
        j += dj
    return lcs


def get_not_lcs(elements1, elements2):
    edit_m = get_edit_matrix(elements1, elements2, swap_weight_func=lcs_swap_weight)
    steps = get_steps(edit_m)
    i, j = 0, 0
    not_lcs1, not_lcs2 = [], []
    for di, dj in steps:
        if (di, dj) == (1, 1) and elements1[i] != elements2[j]:
            not_lcs1.append(elements1[i])
            not_lcs2.append(elements2[j])
        elif (di, dj) == (1, 0):
            not_lcs1.append(elements1[i])
        elif (di, dj) == (0, 1):
            not_lcs2.append(elements2[j])
        i += di
        j += dj
    return not_lcs1, not_lcs2


def diff(path1, path2):
    with open(path1, encoding="utf-8") as f1, open(path2, encoding="utf-8") as f2:
        for i, (l1, l2) in enumerate(zip_longest(f1, f2, fillvalue="")):
            if l1 != l2:
                d1, d2 = get_not_lcs(l1, l2)
                l1 = l1[:-1] if l1.endswith("\n") else l1
                l2 = l2[:-1] if l2.endswith("\n") else l2
                print(f"Line {i + 1}:")
                print(f"\tFile1: {l1}")
                print(f"\t\tNot in lcs: {d1}")
                print(f"\tFile2: {l2}")
                print(f"\t\tNot in lcs: {d2}")


def main():
    str1 = "abcdef"
    str2 = "acbcf"
    el1 = [1, 2, 3, 0, 3]
    el2 = [2, 3, 1, 1, 3, 3]
    print(get_lcs(str1, str2))
    print(get_lcs(el1, el2))
    print(get_not_lcs(el1, el2))


if __name__ == '__main__':
    main()
