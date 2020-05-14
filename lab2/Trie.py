from lab2.shared import add_marker


class Node:
    def __init__(self, char, parent=None, children=None, link=None, depth=0):
        self.char = char
        self.parent = parent
        self.children = dict() if children is None else children
        self.link = link
        self.depth = depth

    def __contains__(self, key):
        return key in self.children

    def __getitem__(self, key):
        return self.children[key]

    def create_and_add_child(self, char):
        if char in self.children:
            print("Adding child with char that already exists")
            exit(1)
        child = Node(parent=self, char=char, depth=self.depth + 1)
        self.children[char] = child
        return child


class Trie:
    def __init__(self, string=None):
        self.root = Node(char=None, depth=0)
        self.root.link = self.root
        self.root.parent = None
        if string is not None:
            self.build(string)

    def __contains__(self, suffix):
        return self.find_prefix(suffix, 0)[1] == len(suffix)

    def build(self, string):
        string = add_marker(string)

        head = self.root
        for i in range(len(string)):
            leaf = self.add(string, i, head)
            head = self.up_link_down(leaf)

    def find_prefix(self, string, suffix_start, start_node=None):
        node = start_node if start_node else self.root
        for i in range(suffix_start, len(string)):
            if string[i] not in node:
                return node, i
            node = node[string[i]]
        return node, len(string)

    @staticmethod
    def add(string, suffix_idx, head):
        leaf = head
        for i in range(suffix_idx + head.depth, len(string)):
            leaf = leaf.create_and_add_child(string[i])
        return leaf

    def up_link_down(self, leaf):
        char_stack = []
        curr_node = leaf
        while curr_node.link is None:
            char_stack.append(curr_node.char)
            curr_node = curr_node.parent

        # found link changing branch
        head = curr_node.link
        if curr_node is self.root:
            char = char_stack.pop()
            self.root[char].link = self.root
            curr_node = self.root[char]

        while char_stack and char_stack[-1] in head:
            char = char_stack.pop()
            curr_node = curr_node[char]
            head = head[char]
            curr_node.link = head
        return head
