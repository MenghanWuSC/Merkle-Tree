#!/usr/bin/python3

import sys, hashlib

# Class: each node of Merkle Tree
class MerkleTreeNode:
    def __init__(self, key, hash=None):
        # Key of each node
        self.key = key
        # Hash value: SHA-256 of each node
        if hash == None:
            self.hash = hashlib.sha256(key.encode('utf-8')).hexdigest()
        else:
            self.hash = hash
        # Key of the left child
        self.left = None
        # Key of the right child
        self.right = None


# Global: data of Merkle Tree
# {'key': node} by dictionary
MerkleTree = {}
# [0] 'Root' of Merkle Tree
MerkleTreeRoot = None
# [ ['key's] ] in BFS order
MerkleTreeBFS = []


def buildMerkleTree(treeNodes:list):
    """
    To build a Merkle Tree especially with the dictionary 'key' mapping,
        using 'bottom-up' method.
    Global: MerkleTree, MerkleTreeRoot
    """
    # Pre-condition
    global MerkleTree, MerkleTreeRoot
    if len(treeNodes) <= 0:
        assert False
    elif len(treeNodes) == 1:
        MerkleTree[treeNodes[0]] = MerkleTreeNode(treeNodes[0])
        MerkleTreeRoot = MerkleTree[treeNodes[0]]
        return

    # Prepare 'leaf' nodes of Merkle Tree from the given list
    for i in treeNodes:
        MerkleTree[i] = MerkleTreeNode(i)

    # Start from at least 2 nodes
    while len(treeNodes) >= 2:
        parentKey = None
        parentList = []
        # For every 2 first nodes, do the concatenation & hash
        for i in range(1, len(treeNodes), 2):
            parentKey = MerkleTree[treeNodes[i-1]].hash +  MerkleTree[treeNodes[i]].hash
            MerkleTree[parentKey] = MerkleTreeNode(parentKey)
            MerkleTree[parentKey].left = treeNodes[i-1]
            MerkleTree[parentKey].right = treeNodes[i]
            # Prepare 'parent' nodes
            parentList.append(parentKey)
            # Handle the odd number of parent nodes
            if i+1 == len(treeNodes)-1:
                parentList.append(treeNodes[i+1])
                break
        # Renew the loop condition
        treeNodes = parentList
    # After divided processing by 2 only 'root' be left [0]
    assert len(treeNodes) == 1
    MerkleTreeRoot = MerkleTree[treeNodes[0]]
# ENDOF: buildMerkleTree()


def BFS_binaryTree(tree:dict, start):
    """
    To plot BFS order of Merkle Tree.
    Global: MerkleTreeBFS
    """
    # Pre-condition
    if tree == {}:
        assert False
    if len(start) == 0:
        assert False

    global MerkleTreeBFS
    # Initialization: next level to be processed nodes 
    nextList = [start]

    # Until nextList NONE
    while nextList:
        # Specifically record the size in each level of Merkle Tree
        currentKey = None
        currentList = []
        currentSize = len(nextList)
        while currentSize > 0:
            # Pop waiting
            currentKey = nextList.pop(0)
            currentList.append(currentKey)
            currentSize -= 1
            # See if the left child is needed
            if tree[currentKey].left != None:
                nextList.append(tree[currentKey].left)
            # See if the right child is needed
            if tree[currentKey].right != None:
                nextList.append(tree[currentKey].right)
        # Update each level's list into BFS
        MerkleTreeBFS.append(currentList)
# ENDOF: BFS_binaryTree()


def drawMerkleTree(tree:dict, BFS:list, filePtr:"I/O"):
    """
    To draw a Merkle Tree by BFS order.
    I/O: Output to filePtr
    """
    # Pre-condition
    if tree == {}:
        assert False
    if BFS == []:
        assert False
    
    filePtr.write("*** This is for Merkle Tree user-friendly graph in 'BFS' order. *** \n")
    filePtr.write("*** Levels start from Root [0] to leafs [log'n] *** \n")
    filePtr.write("*** e.g. Level(n): Hash [key] <left,right>:childs \n")

    # For each level in BFS order
    for i in range(0, len(BFS)):
        for j in BFS[i]:
            # Print the leaf nodes: Level(n): {hash} [key]
            filePtr.write("Level("+ str(i) + "): " + tree[j].hash + " [" + j + "]")
            # Add <left,right>:childs if available
            if tree[j].left != None and tree[j].right != None:
                filePtr.write(" <" + tree[j].left + "," + tree[j].right + ">")
            filePtr.write(" \n")
# ENDOF: drawMerkleTree()


# === Main ===
# Pre-condition
try:
    inputString = sys.argv[1]
    if len(sys.argv) != 2: raise IndexError
    if inputString[0:1] != "[" or inputString[len(inputString)-1:len(inputString)] != "]": raise ValueError
    inputString = inputString[1:len(inputString)-1]
    treeNodes = inputString.split(",")
    if len(treeNodes) >= 2:
        if treeNodes[1][0:1] == " ": raise ValueError 
except:
    print("\nUsage:")
    print("\t./buildmtree.py [node_1,node_2,...,node_n]")
    sys.exit(1)

# Execute building: dictionary and Root of Merkle Tree
buildMerkleTree(treeNodes)

# Execute BFS: Merkle Tree in order
BFS_binaryTree(MerkleTree, MerkleTreeRoot.key)

# Execute drawing: a Merkle Tree by BFS order
with open("merkle.tree", 'w') as outFile:
    drawMerkleTree(MerkleTree, MerkleTreeBFS, outFile)
