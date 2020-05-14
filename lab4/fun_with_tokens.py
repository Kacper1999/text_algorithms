from spacy.tokenizer import Tokenizer
from spacy.attrs import LOWER, POS, ENT_TYPE, IS_ALPHA
from spacy.tokens import Doc
from spacy.lang.pl import Polish
from lab4.lcs import get_lcs_len
import os
import numpy as np
import tokenize
import random


def get_condemned_tokens(tokens, del_ratio):
    tokens_arr1 = tokens.to_array([LOWER, POS, ENT_TYPE, IS_ALPHA])
    init_len = len(tokens_arr1)
    to_del = round(init_len * del_ratio)
    i_to_del = [random.randint(0, init_len - i - 1) for i in range(to_del)]
    tokens_arr1 = np.delete(tokens_arr1, i_to_del, axis=0)
    output = Doc(tokens.vocab, words=[t.text for i, t in enumerate(tokens) if i not in i_to_del])
    output.from_array([LOWER, POS, ENT_TYPE, IS_ALPHA], tokens_arr1)
    return output


def get_tokens_from_file(path):
    text = []
    with tokenize.open(path) as f:
        for row in f:
            text.append(row)
    text = "".join(text)
    tokenizer = Tokenizer(Polish().vocab)
    return tokenizer(text)


def get_condemned_tokens_lcs_len(path, del_ratio):
    tokens = get_tokens_from_file(path)
    tokens1 = get_condemned_tokens(tokens, del_ratio)
    tokens2 = get_condemned_tokens(tokens, del_ratio)
    t1 = [s.text for s in tokens1]
    t2 = [s.text for s in tokens2]
    return get_lcs_len(t1, t2)


# not sure if this is what I was suppose to do
def save_tokens(tokens, to_path):
    with open(to_path, "w", encoding="utf-8") as f:
        for t in tokens:
            f.write(t.text_with_ws)


def save_condemned_tokens(from_path, del_ratio, to_path1, to_path2):
    tokens = get_tokens_from_file(from_path)
    tokens1 = get_condemned_tokens(tokens, del_ratio)
    tokens2 = get_condemned_tokens(tokens, del_ratio)
    save_tokens(tokens1, to_path1)
    save_tokens(tokens2, to_path2)


def main():
    text_files_dir = "some_txt_files"
    rome_file_name = "romeo_i_julia.txt"
    del_ratio = 0.03
    f1_name = "r1.txt"
    f2_name = "r2.txt"

    from_path = os.path.join(text_files_dir, rome_file_name)
    tokens = get_tokens_from_file(from_path)
    print(len(get_condemned_tokens(tokens, del_ratio)))


if __name__ == '__main__':
    main()
