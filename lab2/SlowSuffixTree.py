import lab2.shared as sh


class SlowSuffixTree(sh.SuffixTreeFrame):
    def build(self, text):
        text = sh.add_marker(text)

        head = self.root
        depth = 0
        for i in range(len(text)):
            if depth == head.depth and text[i + depth] in head:
                head, depth = self.slow_find(text, i, head, depth)
            if head.depth > depth:
                head = self.split_node(text, head, depth)
            self.create_and_add_leaf(text, i, head, depth)
            head = self.root
            depth = 0
