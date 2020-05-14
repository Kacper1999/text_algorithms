import random
import string
from timeit import default_timer as dt

terminal = chr(0xF0000)  # unique last symbol


class Trie:
    class _Node:
        def __init__(self, letter, parent=None, children=None, link=None, pref_len=0):
            self.letter = letter
            self.parent = parent
            self.children = {} if not children else children
            self.link = link
            self.len = pref_len

        def add(self, child):
            if child.letter in self.children:
                raise RuntimeError('Undefined behavior')
            self.children[child.letter] = child

        def __getitem__(self, key):
            return self.children[key]

        def __contains__(self, key):
            return key in self.children

        def __len__(self):
            return self.len

    def __init__(self, text=None):
        self.root = self._Node(letter='', pref_len=0)
        self.root.link = self.root
        self.root.parent = None

        if text:
            self.build(text)

    def _validate_and_add(self, text):
        if text[-1] == terminal:
            return text
        else:
            return text + terminal

    def build(self, text):
        text = self._validate_and_add(text)
        head = self.root

        for i in range(len(text)):
            # if (i+1) % 1000 == 0: print(i+1, '/', len(text))
            leaf = self.add(text, i, head)
            head = self.up_link_down(leaf)

    def add(self, text, suffix_start, head):
        leaf = head
        for i in range(suffix_start + len(head), len(text)):
            new_node = self._Node(parent=leaf, letter=text[i], pref_len=len(leaf) + 1)
            leaf.add(new_node)
            leaf = new_node

        return leaf

    def up_link_down(self, leaf):
        q = []  # works A LOT faster than LifoQueue (on 10^6 elements x30 faster)
        prev_branch = leaf
        while prev_branch.link is None:
            q.append(prev_branch.letter)
            prev_branch = prev_branch.parent

        new_head = prev_branch.link
        if prev_branch is self.root:
            l = q.pop()
            self.root[l].link = self.root
            prev_branch = self.root[l]

        while q and q[-1] in new_head:
            l = q.pop()
            prev_branch = prev_branch[l]
            new_head = new_head[l]
            prev_branch.link = new_head
        return new_head

    def find_prefix(self, text, suffix_start, start_node=None):  # used erlier
        node = start_node if start_node else self.root
        for i in range(suffix_start, len(text)):
            if text[i] not in node:
                return node, i
            else:
                node = node[text[i]]
        return node, len(text)

    def __contains__(self, suffix):
        return self.find_prefix(suffix, 0)[1] == len(suffix)


class DegradedSuffixTree:
    class _Node:
        def __init__(self, letter=None, suffix_start=-1, pref_len=-1, parent=None, children=None):
            self.letter = '' if not letter else letter
            self.parent = parent
            self.start = suffix_start
            self.len = pref_len
            self.children = {} if not children else children
            self.suffix_link = None

        def __len__(self):  # depth in tree, but I do it my way XD
            return self.len  # length of string builded from root to the and of this node

        def __contains__(self, key):
            return key in self.children

        def __getitem__(self, key):
            return self.children[key]

        def __str__(self):
            result = f"char = {self.char}, depth = {self.depth}, idx = {self.idx}"
            for child in self.children.values():
                result += child.__str__()
            return result

        def add(self, child):
            self.children[child.letter] = child

    def __init__(self, text=None):
        self.root = self._Node(suffix_start=0, pref_len=0)
        self.root.suffix_link = self.root
        self.root.parent = self.root

        if text is not None:
            self.build(text)

    def _validate_and_add(self, text):
        if text[-1] == terminal:
            return text
        else:
            return text + terminal

    def build(self, text):
        text = self._validate_and_add(text)

        head = self.root
        pref_len = 0  # length of matched prefix of i'th suffix

        for i in range(len(text)):
            if pref_len == len(head) and text[i + pref_len] in head:
                head, pref_len = self.slow_find(text, i, head, pref_len)

            if len(head) > pref_len:
                head = self.split_node(text, head, pref_len)
            self.create_leaf(text, i, head, pref_len)

            pref_len = 0  # generaly max(0, pref_len - 1) 'cause of Lemma 1 in original paper
            head = self.root
            pref_len = 0

        self.text = text

    def slow_find(self, text, cur_start, head, pref_len):
        # jump to next node
        while pref_len == len(head) and text[cur_start + pref_len] in head:
            head = head[text[cur_start + pref_len]]
            pref_len += 1
            # go until the end of node searching for new head
            while pref_len < len(head) and text[cur_start + pref_len] == text[head.start + pref_len]:
                pref_len += 1
        return head, pref_len

    def split_node(self, text, node, pref_len):
        parent = node.parent
        new_node = self._Node(suffix_start=node.start, pref_len=pref_len,
                              letter=text[node.start + len(parent)], parent=parent)
        parent.add(new_node)
        node.parent = new_node
        node.letter = text[node.start + pref_len]
        new_node.add(node)

        return new_node

    def create_leaf(self, text, suffix_start, head, pref_len):
        leaf = self._Node(suffix_start=suffix_start, pref_len=len(text) - suffix_start,
                          letter=text[suffix_start + pref_len])
        leaf.parent = head
        head.add(leaf)
        return leaf  # just in case

    def __contains__(self, key):
        node = self.root

        for d, l in enumerate(key):
            if d == len(node):
                if l not in node:
                    return False
                node = node[l]
            else:
                if l != self.text[node.start + d]:
                    return False
        return True


class SuffixTree:
    class _Node:
        def __init__(self, letter=None, suffix_start=-1, pref_len=-1, parent=None, children=None):
            self.letter = '' if not letter else letter
            self.parent = parent
            self.start = suffix_start
            self.len = pref_len
            self.children = {} if not children else children
            self.suffix_link = None

        def __len__(self):  # depth in tree, but I do it my way XD
            return self.len  # length of string builded from root to the and of this node

        def __contains__(self, key):
            return key in self.children

        def __getitem__(self, key):
            return self.children[key]

        def __str__(self):
            result = f"char = {self.letter}, depth = {self.len}, idx = {self.start}\n"
            for child in self.children.values():
                result += child.__str__()
            return result

        def add(self, child):
            self.children[child.letter] = child

    def __init__(self, text=None):
        self.root = self._Node(suffix_start=0, pref_len=0)
        self.root.suffix_link = self.root
        self.root.parent = self.root

        if text is not None:
            self.build(text)

    def __str__(self):
        return self.root.__str__()

    def _validate_and_add(self, text):
        if text[-1] == terminal:
            return text
        else:
            return text + terminal

    def build(self, text):
        text = self._validate_and_add(text)

        head = self.root
        pref_len = 0  # length of matched prefix of i'th suffix

        for i in range(len(text)):
            if pref_len == len(head) and text[i + pref_len] in head:
                head, pref_len = self.slow_find(text, i, head, pref_len)

            if len(head) > pref_len:
                head = self.split_node(text, head, pref_len)
            self.create_leaf(text, i, head, pref_len)

            if head.suffix_link is None:
                self.fast_find(text, head, pref_len)
            head = head.suffix_link
            pref_len = len(head)  # generaly max(0, pref_len - 1) 'cause of Lemma 1 in original paper

        self.text = text

    def slow_find(self, text, cur_start, head, pref_len):
        # jump to next node
        while pref_len == len(head) and text[cur_start + pref_len] in head:
            head = head[text[cur_start + pref_len]]
            pref_len += 1
            # go until the end of node searching for new head
            while pref_len < len(head) and text[cur_start + pref_len] == text[head.start + pref_len]:
                pref_len += 1
        return head, pref_len

    def split_node(self, text, node, pref_len):
        parent = node.parent
        new_node = self._Node(suffix_start=node.start, pref_len=pref_len,
                              letter=text[node.start + len(parent)], parent=parent)
        parent.add(new_node)
        node.parent = new_node
        node.letter = text[node.start + pref_len]
        new_node.add(node)

        return new_node

    def create_leaf(self, text, suffix_start, head, pref_len):
        leaf = self._Node(suffix_start=suffix_start, pref_len=len(text) - suffix_start,
                          letter=text[suffix_start + pref_len])
        leaf.parent = head
        head.add(leaf)
        return leaf  # just in case

    def fast_find(self, text, head, pref_len):
        next_head = head.parent.suffix_link

        while len(next_head) < pref_len - 1:
            next_head = next_head[text[head.start + len(next_head) + 1]]
        if len(next_head) > pref_len - 1:
            next_head = self.split_node(text, next_head, pref_len - 1)
        head.suffix_link = next_head

    def __contains__(self, key):
        node = self.root

        for d, l in enumerate(key):
            if d == len(node):
                if l not in node:
                    return False
                node = node[l]
            else:
                if l != self.text[node.start + d]:
                    return False
        return True


S1 = "bbb$"
S2 = "aabbabd"
S3 = "ababcd"
S4 = "abcbccd"
with open("1997_714.txt", encoding="utf8") as f:
    S5 = f.read()
TESTS = [S1, S2, S3, S4, S5]
TESTS_NUM = len(TESTS)


def hard_coded_test(test_class):
    tests = ["bab", "aabba", "bbab", "abb", "aaaa", "sk", "aabbabd"]
    for i, test in enumerate(tests):
        result = test in S2
        tmp = test_class(test)
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
    hard_coded_test(Trie)
    correctness_test(SuffixTree, TESTS_NUM)
    time_test(SuffixTree, TESTS_NUM)
    # print()
    # print("SlowSuffixTree tests:")
    # hard_coded_test(Trie)
    # correctness_test(SlowSuffixTree, TESTS_NUM)
    # time_test(SlowSuffixTree, TESTS_NUM)


def main():
    tests = ["bab", "aabba", "bbab", "abb", "aaaa", "sk", "aabbabd"]
    test = tests[-1]
    tmp = SuffixTree(test)
    print(tmp)
    # main_test()


if __name__ == "__main__":
    main()
