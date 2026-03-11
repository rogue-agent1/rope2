#!/usr/bin/env python3
"""rope2 — Rope data structure for efficient string editing. Zero deps."""

class RopeNode:
    __slots__ = ('left', 'right', 'text', 'weight')
    def __init__(self, text=None):
        self.left = self.right = None
        self.text = text
        self.weight = len(text) if text else 0

class Rope:
    LEAF_MAX = 32
    def __init__(self, text=""):
        self.root = self._build(text) if text else None
        self.length = len(text)

    def _build(self, text):
        if len(text) <= self.LEAF_MAX:
            return RopeNode(text)
        mid = len(text) // 2
        node = RopeNode()
        node.left = self._build(text[:mid])
        node.right = self._build(text[mid:])
        node.weight = mid
        return node

    def _collect(self, node):
        if not node: return ""
        if node.text is not None: return node.text
        return self._collect(node.left) + self._collect(node.right)

    def __str__(self): return self._collect(self.root)
    def __len__(self): return self.length

    def char_at(self, idx):
        def _at(node, i):
            if node.text is not None: return node.text[i]
            if i < node.weight: return _at(node.left, i)
            return _at(node.right, i - node.weight)
        return _at(self.root, idx)

    def concat(self, other):
        r = Rope()
        node = RopeNode()
        node.left = self.root
        node.right = other.root
        node.weight = self.length
        r.root = node
        r.length = self.length + other.length
        return r

    def split(self, idx):
        left_parts, right_parts = [], []
        def _split(node, i):
            if not node: return
            if node.text is not None:
                if i > 0: left_parts.append(node.text[:i])
                if i < len(node.text): right_parts.append(node.text[i:])
                return
            if i <= node.weight:
                _split(node.left, i)
                right_parts.append(self._collect(node.right))
            else:
                left_parts.append(self._collect(node.left))
                _split(node.right, i - node.weight)
        _split(self.root, idx)
        return Rope("".join(left_parts)), Rope("".join(right_parts))

    def insert(self, idx, text):
        l, r = self.split(idx)
        return l.concat(Rope(text)).concat(r)

    def delete(self, start, end):
        l, _ = self.split(start)
        _, r = self.split(end)
        return l.concat(r)

def main():
    r = Rope("Hello, World!")
    print(f"Rope: '{r}' (len={len(r)})")
    print(f"char_at(7): '{r.char_at(7)}'")
    r2 = r.insert(7, "Beautiful ")
    print(f"Insert: '{r2}'")
    r3 = r2.delete(7, 17)
    print(f"Delete: '{r3}'")
    a, b = Rope("foo"), Rope("bar")
    print(f"Concat: '{a.concat(b)}'")

if __name__ == "__main__":
    main()
