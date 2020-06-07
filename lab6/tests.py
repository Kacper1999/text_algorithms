import os
import sys
import time
import glob
from suffix_trees import STree
from lab6.lecture_dbf import dbf_find, kmr
from lab6.str_dict_dbf import make_dbf, str_dict_dbf_find
from lab6.bin_search_dbf import bin_search_dbf_find
from lab6.get_size import get_size
from lab6.kmp import kmp_string_matching

text_dir = "texts"


def time_fun(fun, precision=4):
    s = time.time()
    output = fun()
    e = time.time()
    return round(e - s, precision)


def test1():
    for file_path in glob.iglob(text_dir + r"\*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

            if file_path == r"texts\1997_714.txt":
                str_dict_dbf_t = "undef"
            else:
                str_dict_dbf_t = time_fun(lambda: make_dbf(text))
            lec_dbf_t = time_fun(lambda: kmr(text))
            sft_t = time_fun(lambda: STree.STree(text))

            print(file_path)
            print("lecture_dbf", "str_dict_dbf", "suffix_tree", sep="\t")
            print(lec_dbf_t, str_dict_dbf_t, sft_t, sep="\t")


def test2():
    for file_path in glob.iglob(text_dir + r"\*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

            lec_label_tables, lec_ref_tables = kmr(text)
            if file_path == r"texts\1997_714.txt":
                str_dict_label_tables, str_dict_ref_tables = "undef", "undef"
            else:
                str_dict_label_tables, str_dict_ref_tables = make_dbf(text)

            print("lecture dbf sizes:")
            print("label tables     ref tables")
            print(get_size(lec_label_tables), get_size(lec_ref_tables), sep="\t")

            print("str_dict dbf sizes:")
            print("label tables     ref tables")
            print(get_size(str_dict_label_tables), get_size(str_dict_ref_tables), sep="\t")


def test3():
    test_patterns_len = [1, 7, 60]
    start_i = [0, 5, 15]

    for file_path in glob.iglob(text_dir + r"\*.txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

            test_patterns = [text[i:i + size] for i, size in zip(start_i, test_patterns_len)]

            if file_path == r"texts\1997_714.txt":
                str_dict_dbf_t = "undef"
            else:
                dbf = make_dbf(text)
                str_dict_dbf_t = [time_fun(lambda: str_dict_dbf_find(pattern, dbf)) for pattern in test_patterns]
            lec_dbf_t = [time_fun(lambda: dbf_find(pattern, text)) for pattern in test_patterns]

            dbf = kmr(text)
            bin_dbf_t = [time_fun(lambda: bin_search_dbf_find(pattern, text, dbf)) for pattern in test_patterns]
            kmp_t = [time_fun(lambda: kmp_string_matching(text, pattern)) for pattern in test_patterns]

            print(file_path)
            print("\tlec_dbf times:")
            print("\t\t", lec_dbf_t)
            print("\tstr_dict_dbf times:")
            print("\t\t", str_dict_dbf_t)
            print("\tbin_search_dbf times:")
            print("\t\t", bin_dbf_t)
            print("\tkmp times:")
            print("\t\t", kmp_t)


def main():
    # test1()
    # test2()
    # test3()
    print(sys.getsizeof(1))


if __name__ == '__main__':
    main()
