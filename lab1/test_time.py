import time
from os.path import join
from os import getcwd
from lab1.naive import naive_string_matching
from lab1.finite_automata import fa_string_matching, transition_table
from lab1.kmp import kmp_string_matching, prefix_function


def string_match_exec_time(function, text, pattern, test_num=10):
    exec_times = []
    for i in range(test_num):
        start = time.time()
        function(text, pattern)
        end = time.time()
        exec_times.append(end - start)

    print(f'Average time: {sum(exec_times) / len(exec_times)} \n')
    return exec_times


def pre_exec_time(function, pattern, test_num=10):
    exec_times = []
    for i in range(test_num):
        start = time.time()
        function(pattern)
        end = time.time()
        exec_times.append(end - start)

    print(f'Average time: {sum(exec_times) / len(exec_times)} \n')
    return exec_times


def get_algorithms_time(text, pattern, test_num=10):
    print("Naive Algorithm")
    print(string_match_exec_time(naive_string_matching, text, pattern, test_num))
    print("Finite Automata Algorithm")
    print(string_match_exec_time(fa_string_matching, text, pattern, test_num))
    print("KMP Algorithm")
    print(string_match_exec_time(kmp_string_matching, text, pattern, test_num))


def get_pre_time(pattern, test_num=10):
    print("Finite Automata Algorithm Pre Processing")
    print(pre_exec_time(transition_table, pattern, test_num))
    print("KMP Algorithm Pre Processing")
    print(pre_exec_time(prefix_function, pattern, test_num))


def main():
    path = getcwd()
    file = "law.txt"
    with open(join(path, file), "r", encoding='utf-8') as f:
        text = f.read()
    pattern = "art"

    text = "a" * int(1e9) + "b"
    # pattern = "ą" * int(1e2) + "a"

    # get_algorithms_time(text, pattern, 3)

    text1 = "b" + "a" * int(1e9)
    text2 = "a" * int(5e8) + "b" + "a" * int(5e8)
    text3 = "a" * int(1e9) + "b"

    start = time.time()
    print(text == text1)
    end = time.time()
    print(end - start)

    start = time.time()
    print(text == text2)
    end = time.time()
    print(end - start)

    start = time.time()
    print(text == text3)
    end = time.time()
    print(end - start)

    # get_pre_time(pattern)


if __name__ == '__main__':
    main()
