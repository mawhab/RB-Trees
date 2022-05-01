
class Node:
    def __init__(self, value, left=None, right=None, parent=None):
        self.value = value
        self.parent = parent
        self.left = left 
        self.right = right
        self.color = 1

    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.value
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.value
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.value
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.value
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


class RBTree:
    def __init__(self, head:Node=None):
        if head == None:
            self.size = 0
        else:
            self.size = 1
        self.head = head

    def insert(self, value):
        self.size += 1
        if self.head == None:
            self.head = Node(value)
            self.head.color = 0
            return
        node = self.search(value=value, insert=True)
        if node==None: # duplicate elemenet
            self.size -= 1
            return -1
        if node.value>value:
            node.left = Node(value=value, parent=node)
            self.fix(node.left)

        elif node.value<value:
            node.right = Node(value=value, parent=node)
            self.fix(node.right)

    def search(self, value, insert=False):
        temp = self.head
        while True:
            if temp == None:
                return None
            if temp.value < value:
                if temp.right == None and insert:
                    return temp
                temp = temp.right
            elif temp.value > value:
                if temp.left == None and insert:
                    return temp
                temp = temp.left
            else:
                if insert:
                    print(f"ERROR: word already exists ({temp.value})")
                    return None
                return temp

    def fix(self, node:Node):
        if node.color == 0:
            return
        if node == self.head:
            node.color = 0
            return
        if node.parent.color == 1:
            if node.parent.parent.left == None or node.parent.parent.right == None: # uncle is none == black
                if node.parent.right == node: # if this is a right child
                    if node.parent.parent.left == node.parent: # if parent is a left child --> left right case
                        self.leftRotate(node.parent)
                        self.fix(node.left)
                        return
                    else: # right right case
                        node.parent.color = 0
                        node.parent.parent.color = 1
                        self.leftRotate(node.parent.parent)
                        return
                else: # if this is a left child
                    if node.parent.parent.right == node.parent: # if parent is a right child --> right left case
                        self.rightRotate(node.parent)
                        self.fix(node.right)
                        return
                    else: # left left case
                        node.parent.color = 0
                        node.parent.parent.color = 1
                        self.rightRotate(node.parent.parent)
                        return
            else:
                if node.parent.parent.left.color == node.parent.parent.right.color: # if both parent and uncle are red
                    node.parent.parent.left.color = 0
                    node.parent.parent.right.color = 0
                    node.parent.parent.color = 1
                    self.fix(node.parent.parent)
                    return

# left rotate around parent
            
    def leftRotate(self, y:Node):
        x = y.right
        y.right = x.left
        if y.right != None:
            y.right.parent = y
        x.parent = y.parent
        if x.parent == None:
            self.head = x
            # x.parent.left = x
        elif y.parent.right == y:
            y.parent.right = x
        else:
            y.parent.left = x
        y.parent = x
        x.left = y

    def rightRotate(self, x:Node):
        y = x.left
        x.left = y.right
        if x.left != None:
            x.left.parent = x
        y.parent = x.parent
        if y.parent == None:
            self.head = y
            # y.parent.right = y
        elif x.parent.right == x:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def getTreeHeight(self, node:Node):
        if node == None:
            return -1
        return max(self.getTreeHeight(node.left), self.getTreeHeight(node.right)) + 1

    def printTreeHeight(self):
        print(f'height: {self.getTreeHeight(self.head)}')

    def printTreeSize(self):
        print(f'size: {self.size}')


def printTree(head:Node):
    if head == None:
        return
    print(head.value)
    printTree(head.left)
    printTree(head.right)

def loadFile(tree:RBTree):
    with open('EN-US-Dictionary.txt') as f:
        lines = f.readlines()
        for line in lines:
            if tree.insert(line) != -1:
                tree.printTreeHeight()
                tree.printTreeSize()


tree = RBTree()

loadFile(tree)

# printTree(tree.head)

# tree.head.display()

tree.printTreeHeight()

tree.printTreeSize()