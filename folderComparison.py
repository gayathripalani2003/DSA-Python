import os
import hashlib

#Generic Tree Node
class GenericTreeNode:
    def __init__(self, data, is_file):
        self.data = data  #Stores file hash (or) Folder name 
        self.is_file = is_file
        self.children = None  #Childrens - Linked List

#Linked List Node - Childrens are stored as this.
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        
#Linked List Implementation - Childrens of a generic node.
class LinkedList:
    
    def __init__(self):
        self.head = None


    def insert(self, data): #Insert at the end.
        if self.head is None:
            self.head = Node(data)
        else:
            temp = self.head
            while temp.next is not None:
                temp = temp.next
            temp.next = Node(data)

#Calculate the md5 checksum of the given file
def md5(file_path):
    
    hash_md5 = hashlib.md5()
    
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(4096)#Read 4096 bytes
            if not chunk:   #chunk is empty - means end of the file 
                break
            
            hash_md5.update(chunk)#Update MD5
            
    return hash_md5.hexdigest()



class FolderTreeBuild:
    def buildTree(self, folderPath):
        if not os.path.exists(folderPath):
            print("folder path doesn't exists")
            return None

        rootName = os.path.basename(folderPath)
        if rootName == '':
            rootName = folderPath  

        root = GenericTreeNode(rootName, is_file=False)
        children = LinkedList()

        
        folder = sorted(os.listdir(folderPath))  #Sort alphabetically
        for f in folder:
            fullPath = os.path.join(folderPath, f) # f - file or folder
            if os.path.isdir(fullPath):#Folder 
                child_node = self.build_tree(fullPath)
            else:#file
                file_hash = md5(fullPath)
                if file_hash is None:
                    continue
                child_node = GenericTreeNode(file_hash, is_file=True)
            children.insert(child_node)

        root.children = children.head
        return root

class FolderCompare:
    def __init__(self, root1, root2):
        self.root1 = root1
        self.root2 = root2

    def are_identical(self):
        return self.compare(self.root1, self.root2)

    def compare(self, node1, node2):
        if node1 is None and node2 is None: 
            return True
        if node1 is None or node2 is None:
            return False
        if node1.data != node2.data or node1.is_file != node2.is_file:
            return False

        child1 = node1.children
        child2 = node2.children

        while child1 is not None and child2 is not None:
            if not self.compare(child1.data, child2.data):
                return False
            child1 = child1.next
            child2 = child2.next

        if child1 is not None or child2 is not None:
            return False

        return True

def check_if_folders_are_identical(folder1_path, folder2_path):
    builder = FolderTreeBuild()
    root1 = builder.buildTree(folder1_path)
    root2 = builder.buildTree(folder2_path)

    comparator = FolderCompare(root1, root2)

    if comparator.are_identical():
        print("Folders are IDENTICAL")
    else:
        print("Folders are NOT IDENTICAL")


# Check - Test
folder1 = r"C:\Users\gayat\OneDrive\Desktop\career\FD\Backend Developer\NZWalks.Web\NZWalks.API\Controllers"
folder2 = r"C:\Users\gayat\OneDrive\Desktop\career\FD\Backend Developer\NZWalks\Controllers"

check_if_folders_are_identical(folder1, folder2)
