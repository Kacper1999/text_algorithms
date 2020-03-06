"""Knuth-Morris-Pratt algorithm"""


def prefix_function(pattern):
    pi = [0]
    k = 0
    for q in range(1, len(pattern)):
        while k > 0 and pattern[k] != pattern[q]:
            k = pi[k - 1]
        if pattern[k] == pattern[q]:
            k = k + 1
        pi.append(k)
    return pi


def kmp_string_matching(text, pattern):
    pi = prefix_function(pattern)
    q = 0
    valid_shifts = []
    for s in range(len(text)):
        while q > 0 and pattern[q] != text[s]:
            q = pi[q - 1]
        if pattern[q] == text[s]:
            q = q + 1
        if q == len(pattern):
            valid_shifts.append(s)
            q = pi[q - 1]
            # print(f"Shift {s - len(pattern) + 1} is valid")
    return valid_shifts
