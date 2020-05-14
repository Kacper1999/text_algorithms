import random


class Tree:
    def __init__(self):
        self.root = Node("Root")

    def __str__(self):
        return self.root.tree_repr()


class Node:
    def __init__(self, representation, parent=None):
        self.parent = parent
        self.repr = representation
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def create_child(self):
        self.children.append(Node(str(len(self.children))))

    def create_random_children(self, nodes_num):
        if nodes_num <= 0:
            return
        if self.children:
            print("calling random children on a node with children")
            return
        curr_nodes_num = random.randint(1, 4)
        curr_nodes_num = curr_nodes_num if curr_nodes_num <= nodes_num else nodes_num
        nodes_num -= curr_nodes_num
        for _ in range(curr_nodes_num):
            self.create_child()

        children_per_node = nodes_num // curr_nodes_num
        excess = nodes_num % curr_nodes_num

        for i, child in enumerate(self.children):
            if i == 0:
                child.create_random_children(children_per_node + excess)
            else:
                child.create_random_children(children_per_node)

    def tree_repr(self, depth=0):
        output = self.repr
        for child in self.children:
            output += "\n|---" + '----' * depth + child.tree_repr(depth + 1)
        return output

    def __str__(self):
        return self.repr


def random_tree(nodes_num):
    if nodes_num <= 0:
        return None
    t = Tree()
    t.root.create_random_children(nodes_num - 1)
    return t


def main():
    t = random_tree(10)
    print(t)
    print("end")
    t = Tree()
    t.root.create_child()
    t.root.children[0].create_child()
    print(t)


if __name__ == '__main__':
    main()
