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
# [strings] connection of Merkle Tree
MerkleTreeConnect = []


def parseMerkleTree(filePtr:"I/O"):
    """
    To prepare a Merkle Tree by parsing the recorded file.
    I/O: Input from filePtr
    Global: MerkleTree, MerkleTreeRoot, MerkleTreeConnect
    """
    # Initialization
    global MerkleTree, MerkleTreeRoot, MerkleTreeConnect

    # For each line in I/O stream
    for line in filePtr:
        lineList = line.split(" ")
        readKey = lineList[2][1:len(lineList[2])-1]
        readLeft = ""
        readRight = ""
        # Leaf format: Level(n): Hash [key]
        if len(lineList) == 4:
            MerkleTree[readKey] = MerkleTreeNode(readKey, lineList[1])
        # Parent format: Level(n): Hash [key] <left,right>:childs
        elif len(lineList) == 5:
            MerkleTree[readKey] = MerkleTreeNode(readKey, lineList[1])
            readLeft = lineList[3][1:lineList[3].find(",")]
            readRight = lineList[3][lineList[3].find(",")+1:len(lineList[3])-1]
            MerkleTree[readKey].left = readLeft
            MerkleTree[readKey].right = readRight
            # Prepare string list of connection
            # e.g. Connect: key = a + b
            tmpString = "Connect: " + readKey + " = " + readLeft + " + " + readRight
            MerkleTreeConnect.append(tmpString)
            # Root format: Level(0)
            if lineList[0][6] == "0":
                MerkleTreeRoot = MerkleTree[readKey]
        else:
            continue
# ENDOF: parseMerkleTree()


def checkInclusion(tree:dict, root, connect:list, lookup) -> bool:
    """
    To check whether the target is existed & required hashes for 'inclusion' verification.
    """
    # Pre-condition
    if tree == {}:
        assert False
    if root == None:
        assert False
    if connect == []:
        assert False
    if len(lookup) == 0:
        assert False

    # NOT found in Merkle Tree
    if tree.get(lookup) == None:
        print("no")
        return False
    # Found & Query the required nodes
    query = lookup
    hashRequired = []
    # Until 'query' reach the Root of Merkle Tree
    while query != root.key:
        found = [s for s in connect if query in s]
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
    # *For this project: print additional 'Root' hash for proof
    print("yes", hashRequired, "Root:["+ root.hash +"]")
    return True
# ENDOF: checkInclusion()


# === Main ===
# Pre-condition
try:
    inputString = sys.argv[1]
    if len(sys.argv) != 2: raise IndexError
except:
    print("\nUsage:")
    print("\t./checkinclusion.py keyname")
    sys.exit(1)

try:
    # I/O: Input the record file building Merkle Tree
    with open("merkle.tree", 'r') as inFile:
        parseMerkleTree(inFile)
except:
    print("\nWARNING: should execute 'buildmtree.py' first!")
    sys.exit(2)

# Execute checking: inclusion of the target in an existed Merkle Tree
checkInclusion(MerkleTree, MerkleTreeRoot, MerkleTreeConnect, inputString)
