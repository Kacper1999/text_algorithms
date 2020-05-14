import lab2.shared as sh


class SuffixTree(sh.SuffixTreeFrame):
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
            if head.link is None:
                self.fast_find(text, head, depth)
            head = head.link
            depth = head.depth

    def fast_find(self, text, head, depth):
        next_head = head.parent.link

        while next_head.depth < depth - 1:
            next_head = next_head[text[head.idx + next_head.depth + 1]]
        if next_head.depth > depth - 1:
            next_head = self.split_node(text, next_head, depth - 1)
        head.link = next_head
