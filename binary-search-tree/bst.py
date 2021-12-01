class Node:
    """Simple class that represents a BST node"""
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    """Class that represents a full binary search tree"""
    def __init__(self):
        self.root = None
    
    def insert(self, keys):
        """Inserts a list of keys into the BST recursively"""
        def insert_helper(node, key):
            if node is None:
                return Node(key)
            if key < node.key:
                node.left = insert_helper(node.left, key)
            else:
                node.right = insert_helper(node.right, key)
            return node

        for key in keys:
            self.root = insert_helper(self.root, key)
    
    def __init__(self, keys):
        self.root = None
        self.insert(keys)
    
    def search(self, key):
        """Returns a list of nodes containing the path from root to target node"""
        path = []
        def search_helper(node, key):
            if node is None:
                return None
            path.append(node)
            if key < node.key:
                return search_helper(node.left, key)
            elif key > node.key:
                return search_helper(node.right, key)
            else:
                return node
        
        return search_helper(self.root, key), path[:-1]