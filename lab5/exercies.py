from lab5.pattern_matching_in_2d import f_2d_match, los_2d_match
from lab5.aho_corasick import Automaton
import numpy as np
from PIL import Image
import time
import cv2
import os

test_dir = os.path.join(os.getcwd(), "test_files")
txt_f_name = "haystack.txt"
png_f_name = "haystack.png"

txt_f_path = os.path.join(test_dir, txt_f_name)
png_f_path = os.path.join(test_dir, png_f_name)

# additional files w and w_b are too big to give true results but we can add them for fun
letter_f_names = map(lambda x: x + ".png", ["b", "d", "g", "y"])
letter_f_paths = [os.path.join(test_dir, lfn) for lfn in letter_f_names]

patterns_f_names = map(lambda x: x + ".png", ["b", "pattern", "bio", "letter"])
patterns_f_path = [os.path.join(test_dir, pfn) for pfn in patterns_f_names]


def ex2():
    output = []
    with open(txt_f_path) as f:
        prev_row = list(f.__next__())
        for i, curr_row in enumerate(f):
            curr_row = list(curr_row)
            if prev_row[-1] == "\n":
                del prev_row[-1]
            for j, char in enumerate(prev_row):
                try:
                    if curr_row[j] == char:
                        output.append((char, i, j))
                except IndexError:
                    continue
            prev_row = curr_row
    return output


def ex3():
    return f_2d_match(txt_f_path, ["th", "th"]), f_2d_match(txt_f_path, ["t h", "t h"])


def ex4():
    output = []
    image = img_to_los(png_f_path)
    for lfp in letter_f_paths:
        pattern = img_to_los(lfp)
        tmp = los_2d_match(image, pattern)
        output.append([tmp])
    return output


def ex5():
    image = img_to_los(png_f_path)
    pattern = img_to_los(os.path.join(test_dir, "pattern.png"))
    return los_2d_match(image, pattern)


def time_fun(fun, p=True):
    s = time.time()
    fun()
    e = time.time()
    if p:
        print(e - s)
    return e - s


def ex6():
    image = img_to_los(png_f_path)
    for p_path in patterns_f_path:
        pattern = img_to_los(p_path)
        with Image.open(p_path) as p:
            print("Pattern resolution:", p.size)
        print("automaton make time:")
        time_fun(lambda: Automaton(set(row for row in pattern)))
        print("search time:")
        automaton = Automaton(set(row for row in pattern))
        time_fun(lambda: los_2d_match(image, pattern, automaton))


def ex7():
    image = img_to_los(png_f_path)
    img_len = len(image)
    divisors = [2, 4, 8]
    for divisor in divisors:
        pattern = img_to_los(letter_f_paths[0])
        print("search time:")
        automaton = Automaton(set(row for row in pattern))
        chunk = img_len // divisor
        whole_t = 0
        for i in range(divisor):
            whole_t += time_fun(lambda: los_2d_match(image[i * chunk:(i + 1) * chunk], pattern, automaton))
        print("whole time:", whole_t)


# I've allowed myself to convert the png to pgm as the text doesn't need rgba (I hope it's faster that way)
def img_to_los(file_path):
    img = np.array(cv2.imread(file_path, cv2.IMREAD_GRAYSCALE))
    return ["".join([f"{x:03d}" for x in row]) for row in img]


def main():
    # for match in ex2():
    #     print(match)
    # print(ex3())
    # for matches in ex4():
    #     print(len(matches))
    # ex5()
    ex6()
    ex7()


if __name__ == '__main__':
    main()
