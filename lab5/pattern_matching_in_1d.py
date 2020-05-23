import numpy as np


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


def kmp_pattern_matching(seq, pattern):
    pi = prefix_function(pattern)
    q = 0
    valid_shifts = []
    for s in range(len(seq)):
        while q > 0 and pattern[q] != seq[s]:
            q = pi[q - 1]
        if pattern[q] == seq[s]:
            q = q + 1
        if q == len(pattern):
            valid_shifts.append(s - 1)
            q = pi[q - 1]
    return valid_shifts
