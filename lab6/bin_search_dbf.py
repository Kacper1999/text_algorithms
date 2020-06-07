import math
from lab6.lecture_dbf import kmr

# https://en.wikipedia.org/wiki/Private_Use_Areas pretty nice
marker1 = chr(0xF0000)
marker2 = chr(0xF0001)


def bin_search_dbf(s, text, label_dict, ref_dict: dict):
    s_len = len(s)
    ref_len = len(ref_dict)

    def get_substring():
        return text[i:i + s_len]

    left, right = 0, ref_len - 1

    while left <= right:
        m = left + (right - left) // 2
        i = ref_dict[m]
        if get_substring() > s:
            right = m - 1
        elif get_substring() < s:
            left = m + 1
        else:
            return label_dict[i]
    return -1


def bin_search_dbf_find(pattern, text, dbf):
    label_dicts, ref_dicts = dbf
    output = []

    pattern_len = len(pattern)
    text += marker1 * pattern_len

    if pattern_len & (pattern_len - 1) == 0:  # check if is power of 2, assuming pattern isn't a empty string
        accept_k = bin_search_dbf(pattern, text, label_dicts[pattern_len], ref_dicts[pattern_len])
        if accept_k == -1:
            return []

        for i, k in enumerate(label_dicts[pattern_len]):
            if k == accept_k:
                output.append(i)
    else:
        supp_len = 2 ** math.floor(math.log2(pattern_len))
        label_dict = label_dicts[supp_len]
        ref_dict = ref_dicts[supp_len]

        gap_len = pattern_len - supp_len

        accept_k1 = bin_search_dbf(pattern[:supp_len], text, label_dict, ref_dict)
        accept_k2 = bin_search_dbf(pattern[-supp_len:], text, label_dict, ref_dict)
        if accept_k1 == -1 or accept_k2 == -1:
            return []

        for i, k in enumerate(label_dict):
            if k == accept_k1 and accept_k2 == label_dict[i + gap_len]:
                output.append(i)
    return output


def main():
    text = "abbabbaba"
    dbf = kmr(text)
    output = bin_search_dbf_find("abbaba", text, dbf)

    print(dbf[0])
    print(dbf[1])
    print(output)


if __name__ == '__main__':
    main()
