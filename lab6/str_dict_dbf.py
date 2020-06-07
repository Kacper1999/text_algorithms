import math

"""DBF - dictionary of basic factors"""

# https://en.wikipedia.org/wiki/Private_Use_Areas pretty nice
marker1 = chr(0xF0000)
marker2 = chr(0xF0001)


def make_dbf(text):
    text_len = len(text)
    text += marker1 * text_len
    part_len = 1

    label_tables = []
    ref_tables = []
    while part_len < text_len:
        unique_parts_num = 0
        curr_label_arr = []
        curr_ref_dict = dict()

        for i in range(text_len):
            curr_part = text[i:i + part_len]
            if curr_part not in curr_ref_dict:
                curr_label_arr.append(unique_parts_num)
                curr_ref_dict[curr_part] = unique_parts_num
                unique_parts_num += 1
            else:
                curr_label_arr.append(curr_ref_dict[curr_part])

        label_tables.append(curr_label_arr)
        ref_tables.append(curr_ref_dict)
        part_len *= 2

    return label_tables, ref_tables


def str_dict_dbf_find(pattern, dbf):
    label_tables, ref_tables = dbf
    pattern_len = len(pattern)

    output = []
    i = math.floor(math.log2(pattern_len))
    curr_ref_table = ref_tables[i]
    curr_label_table = label_tables[i]

    if pattern_len & (pattern_len - 1) == 0:
        if pattern in curr_ref_table:
            accept_k = curr_ref_table[pattern]
            for j, k in enumerate(curr_label_table):
                if k == accept_k:
                    output.append(j)
    else:
        supp_len = 2 ** i
        gap_len = pattern_len - supp_len
        s1 = pattern[:supp_len]
        s2 = pattern[-supp_len:]
        if s1 in curr_ref_table and s2 in curr_ref_table:
            accept_k1 = curr_ref_table[s1]
            accept_k2 = curr_ref_table[s2]
            for j, k in enumerate(curr_label_table):
                if accept_k1 == k and accept_k2 == curr_label_table[j + gap_len]:
                    output.append(j)
    return output


def main():
    text = "abbabbaba"
    dbf = make_dbf(text)
    output = str_dict_dbf_find("bbab", dbf)
    print(dbf[0])
    print(dbf[1])

    print(output)


if __name__ == '__main__':
    main()
