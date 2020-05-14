from abc import ABC

# https://en.wikipedia.org/wiki/Private_Use_Areas pretty nice
marker = chr(0xF0000)


def add_marker(text):
    if text[-1] == marker:
        return text
    return text + marker


class Node:
    def __init__(self, char=None, parent=None, children=None, suffix_idx=-1, depth=-1):
        self.char = "" if char is None else char
        self.parent = parent
        self.children = dict() if children is None else children
        self.idx = suffix_idx  # wasn't sure how to name those variables
        self.depth = depth
        self.link = None

    def __getitem__(self, key):
        return self.children[key]

    def __contains__(self, key):
        return key in self.children

    def __str__(self):
        result = f"char = {self.char}, depth = {self.depth}, idx = {self.idx}"
        for child in self.children.values():
            result += child.__str__()
        return result

    def create_and_add_child(self, char):
        child = Node(suffix_idx=self.idx + 1, depth=self.depth + 1,
                     char=char, parent=self)
        self.children[char] = child
        return child

    def add_child(self, child):
        self.children[child.char] = child


class SuffixTreeFrame(ABC):
    def __init__(self, text):
        self.root = Node(suffix_idx=0, depth=0)
        self.root.parent = self.root
        self.root.link = self.root
        self.text = text
        self.build(text)

    def __contains__(self, text):
        curr_node = self.root
        for depth, char in enumerate(text):
            if depth == curr_node.depth:
                if char not in curr_node:
                    return False
                curr_node = curr_node[char]
            else:
                if char != self.text[curr_node.idx + depth]:
                    return False
        return True

    def __str__(self):
        return self.root.__str__()

    def build(self, text):
        print("HI")
        pass

    @staticmethod
    def slow_find(text, cur_idx, head, depth):
        while depth == head.depth and text[cur_idx + depth] in head:
            head = head[text[cur_idx + depth]]
            depth += 1
            while depth < head.depth and text[cur_idx + depth] == text[head.idx + depth]:
                depth += 1
        return head, depth

    def fast_find(self, text, head, depth):
        pass

    @staticmethod
    def create_and_add_leaf(text, suffix_idx, head, depth):
        leaf = Node(suffix_idx=suffix_idx, depth=len(text) - suffix_idx,
                    char=text[suffix_idx + depth], parent=head)
        head.add_child(leaf)
        return leaf

    @staticmethod
    def split_node(text, node, depth):
        parent = node.parent
        new_node = Node(suffix_idx=node.idx, depth=depth,
                        char=text[node.idx + parent.depth], parent=parent)
        parent.add_child(new_node)
        node.parent = new_node
        node.char = text[node.idx + depth]
        new_node.add_child(node)
        return new_node
