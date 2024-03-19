class AVLNode:
    def __init__(self,key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        if node is None:
            return 0
        
        else:
            return node.height
        
    def update_height(self,node):
        if node is not None:
            node.height = 1 + max(self.height(node.left), self.height(node.right))

    def balance_factor(self, node):
        if node is None:
            return 0
        
        else:
            return self.height(node.left) - self.height(node.right)
        
    def rotate_right(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self.update_height(y)
        self.update_height(x)

        return x
    
    def rotate_left(self, x):

        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self.update_height(x)
        self.update_height(y)

        return y
    
    def balance(self, node):
        if node is None:
            return node
        
        self.update_height(node)

        balance = self.balance_factor(node)

        if balance > 1:
            if self.balance_factor(node.left) < 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        
        if balance < -1:
            if self.balance_factor(node.right) > 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_right(node)
        
        return node
    
    def insert(self, root, key):
        if root is None:
            return AVLNode(key)
        
        if key < root.key:
            root.left = self.insert(root.left, key)

        else:
            root.right = self.insert(root.right, key)

        return self.balance(root)
    
    def insert_key(self,key):
        self.root = self.insert(self.root, key)
    
    def inOrderDolasmasi(self, root):
        result = []

        if root:
            result += self.inOrderDolasmasi(root.left)
            result.append(root.key)
            result += self.inOrderDolasmasi(root.right)
        return result
    
    def inOrder(self):
        return self.inOrderDolasmasi(self.root)
    

avl_tree = AVLTree()

keys=[9,5,10,0,6,11,-1,1,2]

for key in keys:
    avl_tree.insert_key(key)

print("Inorder dolasmasi sonucu olusan siralama : " , avl_tree.inOrder())