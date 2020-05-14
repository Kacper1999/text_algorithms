import csv
import editdistance  # https://pypi.org/project/editdistance/0.3.1/
from lab4.edit_dist import edit_dist
from lab4.lcs import diff
import os
import lab4.fun_with_tokens as fwt


def test_dist(print_steps=True):
    with open("test.csv", newline='', encoding='utf8') as csv_f:
        r = csv.reader(csv_f)
        for row in r:
            str1, str2 = row
            print("my edit distance:", edit_dist(str1, str2, print_steps=print_steps))
            print("editdistance.eval:", editdistance.eval(str1, str2))
            print()


def other_ex(original, condemned1, condemned2):
    print("lcs_len:", fwt.get_condemned_tokens_lcs_len(original, 0.03), "\n")
    diff(condemned1, condemned2)


def main():
    text_files_dir = "some_txt_files"
    rome_file_name = "romeo_i_julia.txt"
    del_ratio = 0.03
    f1_name = "r1.txt"
    f2_name = "r2.txt"
    f3_name = "a.txt"
    f4_name = "b.txt"

    from_path = os.path.join(text_files_dir, rome_file_name)
    to_path1 = os.path.join(text_files_dir, f1_name)
    to_path2 = os.path.join(text_files_dir, f2_name)
    to_path3 = os.path.join(text_files_dir, f3_name)
    to_path4 = os.path.join(text_files_dir, f4_name)

    fwt.save_condemned_tokens(from_path, del_ratio, to_path1, to_path2)

    test_dist()

    diff(to_path3, to_path4)
    print("lcs_len:", fwt.get_condemned_tokens_lcs_len(from_path, del_ratio), "\n")

    # not the most clear test
    # other_ex(from_path, to_path1, to_path2)


if __name__ == '__main__':
    main()
