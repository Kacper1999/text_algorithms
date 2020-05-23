class Node:
    def __init__(self, parent, char: str, state: int, accepting: bool = False):
        self.parent = parent
        self.accepting = accepting
        self.depth = 0 if parent is None else parent.depth + 1
        self.char = char
        self.state = state
        self.children = dict()
        self.dict_link = None  # links need to be initialized after every child node is present
        self.miss_link = None

    def add_child(self, char: str, state: int, accepting: bool = False):
        if char in self.children:
            raise (Exception("Trying to add a already existing child"))
        child = Node(self, char, state, accepting)
        self.children[char] = child
        return

    def get_suffix(self, prev_chars: list = None):
        if prev_chars is None:
            prev_chars = []
        if self.is_root():
            return "".join(prev_chars)
        prev_chars.insert(0, self.char)
        return self.parent.get_suffix(prev_chars)

    def update_valid_shifts(self, valid_shifts, i):
        if self.accepting:
            word = self.get_suffix()
            valid_shifts.append((i - len(word), i, word))
        curr_node = self.dict_link
        while curr_node is not None:
            word = curr_node.get_suffix()
            valid_shifts.append((i - len(word), i, word))

            curr_node = curr_node.dict_link

    def bfs(self):
        q = [self]
        while q:
            node = q.pop(0)
            yield node
            for c in node.children.values():
                q.append(c)

    def is_root(self):
        return self.parent is None

    def __str__(self):
        output = ""
        if self.accepting:
            output += "accepting "
        output += f"node: {self.char} state: {self.state} with {len(self.children.keys())} children: \n"
        for child in self.children.values():
            output += (self.depth + 1) * "\t" + child.__str__()
        return output

    def __repr__(self):
        return f"node with state: {self.state}"


class Automaton:
    def __init__(self, patterns: set):
        self.patterns = patterns
        self.root: Node = self.create_automaton(patterns)

    @staticmethod
    def create_automaton(patterns: set):
        state = 0
        root = Node(None, "", state, False)
        for p in patterns:
            curr_node = root
            p_len = len(p)
            for i, char in enumerate(p):
                if not (char in curr_node.children):
                    state += 1
                    curr_node.add_child(char, state)
                curr_node = curr_node.children[char]
                if i == p_len - 1:
                    curr_node.accepting = True

        Automaton.set_miss_links(root)
        Automaton.set_dict_links(root)
        return root

    @staticmethod
    def set_miss_links(root: Node):
        nodes = root.bfs()
        for node in nodes:
            if node.is_root():
                miss_link = node
            elif node.parent.is_root():
                miss_link = root
            else:
                curr_node = node.parent.miss_link
                while not curr_node.is_root() and node.char not in curr_node.children:
                    curr_node = curr_node.miss_link
                miss_link = curr_node.children.get(node.char, root)
            node.miss_link = miss_link

    @staticmethod
    def set_dict_links(root: Node):
        nodes = root.bfs()
        for node in nodes:
            curr_node = node.miss_link
            while not curr_node.is_root():
                if curr_node.accepting or curr_node.dict_link is not None:
                    node.dict_link = curr_node
                    break
                curr_node = curr_node.miss_link

    def get(self, text: str):
        valid_shifts = []
        states = []
        curr_node = self.root
        for i, char in enumerate(text):
            while char not in curr_node.children and not curr_node.is_root():
                curr_node = curr_node.miss_link
            curr_node = curr_node.children.get(char, self.root)
            curr_node.update_valid_shifts(valid_shifts, i + 1)
            states.append(curr_node.state)
        return valid_shifts, states

    def get_last_state(self, text: str):
        return self.get(text)[1][-1]

    def bfs(self):
        return self.root.bfs()

    def __str__(self):
        return self.root.__str__()


def main():
    text = "catcgcgattatt"
    patterns = {"acc", "a", "at", "cat", "gcg", "ctg"}
    a = Automaton(patterns)
    print(a)
    print(a.get(text))


if __name__ == '__main__':
    main()
