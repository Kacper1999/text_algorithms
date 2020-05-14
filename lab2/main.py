import random
import string
from timeit import default_timer as dt

from lab2.SuffixTree import SuffixTree
from lab2.Trie import Trie
from lab2.SlowSuffixTree import SlowSuffixTree

S1 = "bbb$"
S2 = "aabbabd"
S3 = "ababcd"
S4 = "abcbccd"
S5 = "a" * int(1e3) + "b" * int(1e3) + "a" * int(1e2)
with open("1997_714.txt", encoding="utf8") as f:
    S_1 = f.read()
TESTS = [S1, S2, S3, S4, S5, S_1]
TESTS_NUM = len(TESTS)


def hard_coded_test(test_class):
    tests = ["bab", "aabba", "bbab", "abb", "aaaa", "sk", "aabbabd"]
    tmp = test_class(tests[-1])
    for i, test in enumerate(tests):
        result = test in S2
        my_result = test in tmp
        if result == my_result:
            print(f"Hard coded test {i} passed")
        else:
            print(f"Hard coded test {i} failed")


def correctness_test(test_class, tests_num=TESTS_NUM, substring_len=3):
    tests = TESTS[:tests_num]
    for test_num, text in enumerate(tests):
        r_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=substring_len))

        p_start = dt()
        result = r_string in text
        p_end = dt()

        tmp = test_class(text)
        start = dt()
        my_result = r_string in tmp
        end = dt()
        if result == my_result:
            print(f"Test{test_num + 1} passed in: {end - start}s, Python time: {p_end - p_start}")
        else:
            print(f"Test{test_num + 1} failed")
            exit(1)


def time_test(test_class, num_tests=TESTS_NUM):
    tests = TESTS[:num_tests]
    for test_num, text in enumerate(tests):
        print(f"Building tree for test{test_num + 1}")
        start = dt()
        test_class(text)
        end = dt()
        print(f"Built tree for test{test_num + 1} in {end - start}s")


def main_test(do_not_waste_my_time=True):
    trie_tests_num = TESTS_NUM - 1 if do_not_waste_my_time else TESTS_NUM
    print("Trie tests:")
    hard_coded_test(Trie)
    correctness_test(Trie, trie_tests_num)
    time_test(Trie, trie_tests_num)
    print()
    print("SuffixTree tests:")
    hard_coded_test(SuffixTree)
    correctness_test(SuffixTree, TESTS_NUM)
    time_test(SuffixTree, TESTS_NUM)
    print()
    print("SlowSuffixTree tests:")
    hard_coded_test(SlowSuffixTree)
    correctness_test(SlowSuffixTree, TESTS_NUM)
    time_test(SlowSuffixTree, TESTS_NUM)


def main():
    main_test()


if __name__ == "__main__":
    main()
