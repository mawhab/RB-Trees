class RblackNode:
    def __init__(self, val):
        self.red = False
        self.parent = None
        self.val = val
        self.left = None
        self.right = None


class RblackTree:
    def __init__(self):
        self.nil = RblackNode(0)
        self.nil.red = False
        self.nil.left = None
        self.nil.right = None
        self.root = self.nil
        self.size = 0
    
    def search_tree(self,key):
        current = self.root
        while current != self.nil:
            if key < current.val:
                current = current.left
            elif key > current.val:
                current = current.right
            else:
                return print('found')
        return print('Not Found')

    def insert(self, val):
        self.size += 1
        new_node = RblackNode(val)
        new_node.parent = None
        new_node.left = self.nil
        new_node.right = self.nil
        new_node.red = True

        parent = None
        current = self.root
        while current != self.nil:
            parent = current
            if new_node.val < current.val:
                current = current.left
            elif new_node.val > current.val:
                current = current.right
            else:
                self.size-=1
                print('ERROR: Word already exists!')
                return

        new_node.parent = parent
        if parent == None:
            self.root = new_node
            self.fix(self.root)
        elif new_node.val < parent.val:
            parent.left = new_node
            self.fix(parent.left)
        else:
            parent.right = new_node
            self.fix(parent.right)
    
    def fix(self, node:RblackNode):
        if node.red == False:
            return
        if node == self.root:
            node.red = False
            return
        if node.parent.red == True:
            if node.parent.parent.left.red == False or node.parent.parent.right.red == False: # uncle is none == black
                if node.parent.right == node: # if this is a right child
                    if node.parent.parent.left == node.parent: # if parent is a left child --> left right case
                        self.leftRotate(node.parent)
                        self.fix(node.left)
                        return
                    else: # right right case
                        node.parent.red = False
                        node.parent.parent.red = True
                        self.leftRotate(node.parent.parent)
                        return
                else: # if this is a left child
                    if node.parent.parent.right == node.parent: # if parent is a right child --> right left case
                        self.rightRotate(node.parent)
                        self.fix(node.right)
                        return
                    else: # left left case
                        node.parent.red = False
                        node.parent.parent.red = True
                        self.rightRotate(node.parent.parent)
                        return
            else:
                if node.parent.parent.left.red == node.parent.parent.right.red: # if both parent and uncle are red
                    node.parent.parent.left.red = False
                    node.parent.parent.right.red = False
                    node.parent.parent.red = True
                    self.fix(node.parent.parent)
                    return

# left rotate around parent
            
    def leftRotate(self, y:RblackNode):
        x = y.right
        y.right = x.left
        y.right.parent = y
        x.parent = y.parent
        if x.parent == None:
            self.root = x
            # x.parent.left = x
        elif y.parent.right == y:
            y.parent.right = x
        else:
            y.parent.left = x
        y.parent = x
        x.left = y

    def rightRotate(self, x:RblackNode): # x = grandparent
        y = x.left # y = parent
        x.left = y.right
        x.left.parent = x
        y.parent = x.parent
        if y.parent == None:
            self.root = y
            # y.parent.right = y
        elif x.parent.right == x:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y



    def getTreeHeight(self, node:RblackNode):
        if node == None:
            return -1
        return max(self.getTreeHeight(node.left), self.getTreeHeight(node.right)) + 1

    def printTreeHeight(self):
        print(f'height: {self.getTreeHeight(self.root)}')
    
    def printTreeSize(self):
        print(f'size: {self.size}')

    def readFromFile(self, file:str):
        with open(file) as f:
            arr = f.readlines()

        for line in arr:
            line = line.replace('\n', '')
            self.insert(line)


tree = RblackTree()

tree.readFromFile('EN-US-Dictionary.txt')

tree.printTreeHeight()

tree.printTreeSize()