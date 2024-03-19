class TreeNode: #Ağaç için düğüm ve bu düğümün sol ve sağ alt düğümlerini oluşturma.
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def dugumEkle(root, key):
    if root is None:
        return TreeNode(key)
    
    if key < root.key:
        root.left = dugumEkle(root.left, key)
    
    elif key > root.key:
        root.right = dugumEkle(root.right, key)

    return root

root = None
keys = [15,10,20,8,12,17,25]

for key in keys:
    root = dugumEkle(root, key)

def inOrderDolasmasi(root):
    result = []

    if root:
        result += inOrderDolasmasi(root.left)
        result.append(root.key)
        result += inOrderDolasmasi(root.right)

    return result

def preOrderDolasmasi(root):
    result = []

    if root:
        result.append(root.key)
        result += preOrderDolasmasi(root.left)
        result += preOrderDolasmasi(root.right)

    return result

def postOrderDolasmasi(root):
    result = []

    if root:
        result+= postOrderDolasmasi(root.left)
        result += postOrderDolasmasi(root.right)
        result.append(root.key)

    return result


inOrderDolasmasiSonucu = inOrderDolasmasi(root)

print("Inorder dolasmasi : " , inOrderDolasmasiSonucu)

preOrderDolasmasiSonucu = preOrderDolasmasi(root)

print("Preoder dolasmasi : " , preOrderDolasmasiSonucu)

postOrderDolasmasiSonucu = postOrderDolasmasi(root)

print("Postorder dolasmasi : " , postOrderDolasmasiSonucu)