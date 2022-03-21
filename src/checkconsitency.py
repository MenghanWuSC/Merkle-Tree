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


# Global: data of two Merkle Trees
# {'key': node} by dictionary
MerkleTree1 = {}
MerkleTree2 = {}
# [0] 'Root' of Merkle Tree
MerkleTreeRoot1 = None
MerkleTreeRoot2 = None
# [strings] connection of Merkle Tree
MerkleTreeConnect1 = []
MerkleTreeConnect2 = []
# [ ['key's] ] in BFS order
MerkleTreeBFS1 = []
MerkleTreeBFS2 = []


def checkConsistency(treeNodes1:list, treeNodes2:list) -> list:
    """
    To check whether both trees are consistent & required hashes for "consistency proof."
    Global: MerkleTree1&2, MerkleTreeRoot1&2, MerkleTreeConnect1&2, MerkleTreeBFS1&2
    Return: [yes/no, [proof]]
    """
    # Pre-condition
    # ...len(treeNodes1), len(treeNodes2)
    global MerkleTree1, MerkleTree2, MerkleTreeRoot1, MerkleTreeRoot2, MerkleTreeConnect1, MerkleTreeConnect2, MerkleTreeBFS1, MerkleTreeBFS2

    # Prepare 1. & 2. Merkle Tree
    tmpList = buildMerkleTree(treeNodes1)
    MerkleTree1 = tmpList[0]
    MerkleTreeRoot1 = tmpList[1]
    MerkleTreeConnect1 = tmpList[2]
    tmpList = buildMerkleTree(treeNodes2)
    MerkleTree2 = tmpList[0]
    MerkleTreeRoot2 = tmpList[1]
    MerkleTreeConnect2 = tmpList[2]

    # Prepare BFS order of 1. & 2. Merkle Tree
    MerkleTreeBFS1 = BFS_binaryTree(MerkleTree1, MerkleTreeRoot1.key)
    MerkleTreeBFS2 = BFS_binaryTree(MerkleTree2, MerkleTreeRoot2.key)

    # Initialization of return list
    retList = []

    # 1. Check content of subarray
    if checkSubarray(treeNodes1, treeNodes2) == False:
        retList.append("no")
        return retList
    retList.append("yes")
    # 2. Locate those required hashes
    hashRequired = []
    # One Root is NOT completed and included in the other Merkle Tree
    if MerkleTree2.get(MerkleTreeRoot1.key) == None:
        # Both left & right nodes are needed
        hashRequired.append(MerkleTree1[MerkleTreeRoot1.right].hash)
        hashRequired.extend(getInclusion(MerkleTree2, MerkleTreeRoot2, MerkleTreeConnect2, MerkleTreeRoot1.right))
    # One Root is completed and included
    else:    
        hashRequired.extend(getInclusion(MerkleTree2, MerkleTreeRoot2, MerkleTreeConnect2, MerkleTreeRoot1.key))
    retList.append(hashRequired)
    return retList
# ENDOF: checkConsistency()


def buildMerkleTree(treeNodes:list) -> list:
    """
    To build a Merkle Tree using 'bottom-up' method.
    Return: [{Tree}, Root, [Connect]]
    """
    # Pre-condition
    if len(treeNodes) <= 0:
        assert False
    elif len(treeNodes) == 1:
        return [[MerkleTreeNode(treeNodes[0])], MerkleTreeNode(treeNodes[0]), []]

    # Initialization
    tree = {}
    treeRoot = None
    treeConnect = []

    # Prepare 'leaf' nodes of Merkle Tree from the given list
    for i in treeNodes:
        tree[i] = MerkleTreeNode(i)
    # Start from at least 2 nodes
    while len(treeNodes) >= 2:
        parentKey = None
        parentList = []
        # For every 2 first nodes, do the concatenation & hash
        for i in range(1, len(treeNodes), 2):
            parentKey = tree[treeNodes[i-1]].hash + tree[treeNodes[i]].hash
            tree[parentKey] = MerkleTreeNode(parentKey)
            tree[parentKey].left = treeNodes[i-1]
            tree[parentKey].right = treeNodes[i]
            # Prepare string list of connection
            # e.g. Connect: key = a + b
            tmpString = "Connect: " + parentKey + " = " + treeNodes[i-1] + " + " + treeNodes[i]
            treeConnect.append(tmpString)
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
    treeRoot = tree[treeNodes[0]]
    return [tree, treeRoot, treeConnect]
# ENDOF: buildMerkleTree()


def checkSubarray(treeNodes1:list, treeNodes2:list) -> bool:
    """
    To preliminarily check two Merkle Trees in view of subarray.
    Return: True/False
    """
    # Pre-condition
    # ...len(treeNodes1), len(treeNodes2)
    listLong = []
    listShort = []
    verified = 0
    # Decide lists by length
    if len(treeNodes1) > len(treeNodes2):
        listLong = treeNodes1
        listShort = treeNodes2
    else:
        listLong = treeNodes2
        listShort = treeNodes1
    # Only needed the length of the shorter list
    for indexShort in range(0, len(listShort)):
        # Verify elements one by one
        if listShort[indexShort] != listLong[indexShort]:
            return False
        else:
            verified += 1
    # Verified number is passed
    if verified == len(listShort):
        return True
    # Default: should return 'false'
    return False
# ENDOF: checkSubarray()


def getInclusion(tree:dict, root, connect:list, lookup) -> list:
    """
    To locate the "consistency proof."
    Return: [proof]
    """
    # Pre-condition
    if tree == {}:
        assert False
    if root == None:
        assert False
    if connect == []:
        assert False
    if lookup == None:
        assert False
    
    # Found & Query the required nodes
    query = lookup
    hashRequired = []
    # Until 'query' reach the Root of Merkle Tree
    while query != root.key:
        found = [s for s in connect if s.split(" ")[3] == query or s.split(" ")[5] == query]
        assert len(found) == 1
        foundSplit = found[0].split(" ")
        # From 'left' to request 'right'  
        if query == foundSplit[3]:
            hashRequired.append(tree[foundSplit[5]].hash)
        # From 'right' to request 'left'
        elif query == foundSplit[5]:
            hashRequired.append(tree[foundSplit[3]].hash)
        else:
            assert False
        # Move up to parent level & Clean visited connection
        query = foundSplit[1]
        connect.remove(found[0])
    # After query & return answers
    return hashRequired
# ENDOF: getInclusion()


def BFS_binaryTree(tree:dict, start) -> list:
    """
    To plot BFS order of Merkle Tree.
    Return: [[keys]]
    """
    # Pre-condition
    if tree == {}:
        assert False
    if len(start) == 0:
        assert False

    # Initialization
    treeBFS = []
    # Next level to be processed nodes 
    nextList = []
    nextList.append(start)

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
        treeBFS.append(currentList)
    return treeBFS
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
    inputString1 = sys.argv[1]
    inputString2 = sys.argv[2]
    if len(sys.argv) != 3: raise IndexError
    if inputString1[0:1] != "[" or inputString1[len(inputString1)-1:len(inputString1)] != "]": raise ValueError
    if inputString2[0:1] != "[" or inputString2[len(inputString2)-1:len(inputString2)] != "]": raise ValueError
    inputString1 = inputString1[1:len(inputString1)-1]
    inputString2 = inputString2[1:len(inputString2)-1]
    treeNodes1 = inputString1.split(",")
    treeNodes2 = inputString2.split(",")
    if len(treeNodes1) >= 2:
        if treeNodes1[1][0:1] == " ": raise ValueError
    if len(treeNodes2) >= 2:
        if treeNodes2[1][0:1] == " ": raise ValueError
except:
    print("\nUsage:")
    print("\t./checkconsitency.py [node_1,node_2,...,node_n] [node_1,node_2,...,node_n]")
    sys.exit(1)

# Execute checking: consistency of two Merkle Trees
answer = []
answer = checkConsistency(treeNodes1, treeNodes2)
assert len(answer) >= 1
if answer[0] == "yes":
    # *For this project: print additional 'Root' hashes of both older & newer Merkle Tree
    print(answer[0], "olderRoot:["+MerkleTreeRoot1.hash+"]", answer[1], "newerRoot:["+MerkleTreeRoot2.hash+"]")
else:
    print(answer[0])

# Execute drawing: two Merkle Trees by BFS order
with open("merkle.trees", 'w') as outFile:
    outFile.write("*** These are for Merkle Tree user-friendly graphs in 'BFS' order. *** \n")
    outFile.write("*** Levels start from Root [0] to leafs [log'n] *** \n")
    outFile.write("*** e.g. Level(n): Hash [key] <left,right>:childs \n")
    drawMerkleTree(MerkleTree1, MerkleTreeBFS1, outFile)
    outFile.write("-\n")
    drawMerkleTree(MerkleTree2, MerkleTreeBFS2, outFile)
