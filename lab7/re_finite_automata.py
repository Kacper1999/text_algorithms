class Node:
    def __init__(self):
        self.children = dict()

    def add_child(self, char, node):
        if char in self.children:
            raise ValueError("adding already existing connection")
        self.children[char] = node

        

class RegexFA:
    def __init__(self, regex: str):
        self.root = self.build_automata(regex)
        self.accepting_node = None

    def build_automata(self, regex: str):
        pass



def main():
    print()


if __name__ == '__main__':
    main()
