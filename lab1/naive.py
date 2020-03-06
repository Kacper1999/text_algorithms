def naive_string_matching(text, pattern):
    valid_shifts = []
    for s in range(len(text) - len(pattern) + 1):
        if pattern == text[s:s + len(pattern)]:
            valid_shifts.append(s)
            # print(f"Shift {s} is valid")
    return valid_shifts
