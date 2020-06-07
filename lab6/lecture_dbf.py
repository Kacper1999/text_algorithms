import math

"""DBF - dictionary of basic factors"""

# https://en.wikipedia.org/wiki/Private_Use_Areas pretty nice
marker1 = chr(0xF0000)
marker2 = chr(0xF0001)


def sort_rename(seq):
    last_entry = None
    i = 0
    position_to_index = [0] * len(seq)
    first_entry = dict()

    for entry in sorted([(e, i) for i, e in enumerate(seq)]):
        if last_entry and last_entry[0] != entry[0]:
            i += 1
            first_entry[i] = entry[1]

        position_to_index[entry[1]] = i
        if last_entry is None:
            first_entry[0] = entry[1]
        last_entry = entry
    return position_to_index, first_entry


def kmr(text):
    original_len = len(text)
    factor = math.floor(math.log2(original_len))
    padding_len = 2 ** (factor + 1) - 1
    text += marker1 * padding_len

    position_to_index, first_entry = sort_rename(list(text))
    names = {1: position_to_index}
    entries = {1: first_entry}

    for i in range(1, factor):
        power = 2 ** (i - 1)
        new_seq = []
        for j in range(original_len):
            if j + power < len(names[power]):
                new_seq.append((names[power][j], names[power][j + power]))
        position_to_index, first_entry = sort_rename(new_seq)
        names[power * 2] = position_to_index
        entries[power * 2] = first_entry
    return names, entries


def dbf_find(pattern, text):
    names, entries = kmr(pattern + marker2 + text)
    output = []

    pattern_len = len(pattern)

    if pattern_len & (pattern_len - 1) == 0:  # check if is power of 2, assuming pattern isn't a empty string
        accept_k = names[pattern_len][0]
        for i, k in enumerate(names[pattern_len][pattern_len + 1:]):
            if k == accept_k:
                output.append(i)
    else:
        supp_len = 2 ** math.floor(math.log2(pattern_len))

        gap_len = pattern_len - supp_len

        accept_k1 = names[supp_len][0]
        accept_k2 = names[supp_len][gap_len]

        text_names = names[supp_len][pattern_len + 1:]
        for i, k in enumerate(text_names):
            if k == accept_k1 and accept_k2 == text_names[i + gap_len]:
                output.append(i)
    return output


def main():
    text = "abbabbaba"
    output = dbf_find("abbab", text)

    print(kmr(text))


if __name__ == '__main__':
    main()
