operators = [".", "*", "+", "?", "(", ")"]


class ExecNode:
    def __init__(self, content, kind):
        self.type = content
        self.kind = kind


class ExecTree:
    def __init__(self, regex: str):
        self.root = self.build_exec_tree(regex)

    def build_exec_tree(self, regex: str):
        li, ri = 0, 0


def main():
    pass


if __name__ == '__main__':
    main()
