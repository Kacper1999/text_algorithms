from lab5.pattern_matching_in_2d import f_2d_match, lol_2d_match
from PIL import Image
import os

test_dir = os.path.join(os.getcwd(), "test_files")
txt_file_name = "haystack.txt"
png_file_name = "haystack.png"
letter_file_names = map(lambda x: x + ".png", ["b", "e", "w", "m", "w_b"])   # w_b is a bigger version of w (see image)
letter_file_paths = [os.path.join(test_dir, lfn) for lfn in letter_file_names]

txt_file_path = os.path.join(test_dir, txt_file_name)
png_file_path = os.path.join(test_dir, png_file_name)


def ex2():
    output = []
    with open(txt_file_path) as f:
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
    return f_2d_match(txt_file_path, ["th", "th"]), f_2d_match(txt_file_path, ["t h", "t h"])


def ex4():
    def img_to_lol(img):
        def pix_to_str(pixel):
            return "".join([str(x) for x in pixel])

        pix = img.load()
        w, h = img.size
        return [[pix_to_str(pix[x, y]) for x in range(w)] for y in range(h)]

    output = []
    with Image.open(png_file_path) as im:
        image = img_to_lol(im)
        for lfp in letter_file_paths:
            with Image.open(lfp) as letter:
                pattern = img_to_lol(letter)
                print("hi")
                for row in pattern:
                    print(row)
                tmp = lol_2d_match(image, pattern)
                print("hi")
                output += tmp
    return tmp


def main():
    for match in ex2():
        print(match)
    print(ex3())
    ex4()


if __name__ == '__main__':
    main()
