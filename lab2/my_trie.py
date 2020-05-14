from queue import LifoQueue


class Trie:
    def __init__(self, text):
        self.leafs = list()
        self.root = Node(text[0])

        curr_node = self.root
        for char in text[1:]:
            curr_node.create_child(char)
            curr_node = curr_node.get_child(char)
        self.leafs.append(curr_node.get_child(text[-1]))

    def __str__(self):
        result = ""
        result += f"{self.root.letter} at depth: {self.root.depth}\n"
        for child in self.root.children.values():
            result += child.__str__()
        return result


class Node:
    def __init__(self, letter, parent=None):
        self.letter = letter
        self.children = dict()
        self.parent = parent
        self.depth = 0 if parent is None else parent.depth + 1
        self.link = None

    def get_child(self, letter):
        return self.children.get(letter, None)

    def create_child(self, letter):
        self.children[letter] = Node(letter, self)

    def __str__(self):
        result = f"{self.letter} at depth: {self.depth}\n"
        for child in self.children.values():
            result += child.__str__()
        return result


def up_link_down(sibling):
    letters = LifoQueue()
    while sibling is not None and sibling.link is None:
        letters.put(sibling.letter)
        sibling = sibling.parent
    if sibling is None:
        return None, None
    node = sibling.link
    while not letters.empty():
        curr_letter = letters.get()
        if node.get_child(curr_letter):
            node = node.get_child(curr_letter)
            sibling = sibling.get_child(curr_letter)
            sibling.link = node
        else:
            break
    return node, sibling


def graft(node, text, sibling=None):
    for curr_letter in list(text):
        node = node.create_and_add_child(curr_letter)
        if sibling is not None:
            sibling = sibling.get_child(curr_letter)
            sibling.link = node
    return node


def left_to_right(text):
    root = Node("")
    leaf = graft(root, text)
    root.children()[0].link = root
    for i in range(1, len(text)):
        head, sibling = up_link_down(leaf)
        if head is None:
            sibling = root.get_child(text[i - 1])
            sibling.link = root
            head = root
        graft(head, text[i + head.depth:], sibling)


def build_tree_schema(text):
    trie = Trie(text)
    leaf = trie.leafs[0]
    for i in range(1, len(text)):
        suffix = text[i:]
        head = trie.find(suffix, leaf)
        suffix_end = suffix[head.depth():]
        leaf = head.graft(suffix_end)
    return trie


def main():
    text = "hello"
    print(text)
    print(Trie(text))
    print(text)


if __name__ == '__main__':
    main()
