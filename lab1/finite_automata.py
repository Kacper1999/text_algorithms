import re


def transition_table(pattern):
    result = []
    alphabet = set(pattern)
    for q in range(len(pattern) + 1):
        result.append(dict())
        for a in alphabet:
            k = min(len(pattern) + 1, q + 2)
            while True:
                k -= 1
                if re.search(f"{pattern[:k]}$", pattern[:q] + a):
                    break
            result[q][a] = k
    return result


def fa_string_matching(text, pattern):
    valid_shifts = []
    q = 0
    delta = transition_table(pattern)
    alphabet = set(pattern)
    for s in range(len(text)):
        if text[s] not in alphabet:
            q = 0
            continue
        q = delta[q][text[s]]
        if q == len(delta) - 1:
            valid_shifts.append(s)
            # print(f"Shift {s - len(pattern) + 1} is valid")
    return valid_shifts
