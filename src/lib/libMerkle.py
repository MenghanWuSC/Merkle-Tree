

import hashlib
from collections import deque


# Class: each node of Merkle Tree
class MerkleTreeNode:
    def __init__(self, key:str=None):
        self.key = key      # Key of each node
        self.hash = hashlib.sha256(key.encode('utf-8')).hexdigest() if key is not None else None    # Hash value: SHA-256 of each node
        self.left = None    # Key of the left child
        self.right = None   # Key of the right child


# Class: a general instance of Merkle Tree
class MerkleTree:
    def __init__(self, initial=None):
        """
            Build a Merkle Tree from given 1) a list 2) a str to file.
            Instances: {nodeDict}, MerkleTreeRoot
        """
        self.nodeDict = {}
        self.MerkleTreeRoot = MerkleTreeNode()
        # Constructor 1. initialization by nodes
        if isinstance(initial, list):
            # Case: empty list
            if len(initial) == 0: return
            # Case: only one node
            elif len(initial) == 1:
                self.nodeDict[initial[0]] = MerkleTreeNode(initial[0])
                self.MerkleTreeRoot = MerkleTreeNode(initial[0])
                return
            # Else cases: more nodes in list
            # Prepare 'leaf' nodes from given list
            for n in initial:
                self.nodeDict[n] = MerkleTreeNode(n)
            # Start from at least 2 nodes
            nodes = list(initial)
            while len(nodes) >= 2:
                parentKey = ""
                parentList = []
                # For every 2 first nodes, do the concatenation & hash
                for i in range(1, len(nodes), 2):
                    parentKey = self.nodeDict[nodes[i-1]].hash + self.nodeDict[nodes[i]].hash
                    self.nodeDict[parentKey] = MerkleTreeNode(parentKey)
                    self.nodeDict[parentKey].left = nodes[i-1]
                    self.nodeDict[parentKey].right = nodes[i]
                    # Prepare the next run's 'parent' node
                    parentList.append(parentKey)
                    # Check if there is a remaining odd node
                    if i+1 == len(nodes)-1:
                        parentList.append(nodes[i+1])
                        break
                # Renew the loop condition
                nodes = list(parentList)
            # After divided processing by 2 only the root [0] is left
            assert len(nodes) == 1
            self.MerkleTreeRoot = MerkleTreeNode(nodes[0])
            self.MerkleTreeRoot.left = self.nodeDict[nodes[0]].left
            self.MerkleTreeRoot.right = self.nodeDict[nodes[0]].right
        # Constructor 2. initialization from file
        elif isinstance(initial, str):
            with open(initial, mode='r') as filePtr:
                # For each line in I/O stream
                for line in filePtr:
                    lineList = line.split(" ")
                    # Ignore the comments '***'
                    if lineList[0] == "***":
                        continue
                    # Handle the leaf format: Level(n): Hash [key]
                    elif len(lineList) == 4:
                        readKey = lineList[2][1:len(lineList[2])-1]
                        self.nodeDict[readKey] = MerkleTreeNode(readKey)
                    # Handle the parent format: Level(n): Hash [key] <left,right>:childs
                    elif len(lineList) == 5:
                        readKey = lineList[2][1:len(lineList[2])-1]
                        self.nodeDict[readKey] = MerkleTreeNode(readKey)
                        readLeft = lineList[3][1:lineList[3].find(",")]
                        readRight = lineList[3][lineList[3].find(",")+1:len(lineList[3])-1]
                        self.nodeDict[readKey].left = readLeft
                        self.nodeDict[readKey].right = readRight
                        # Get the root: Level(0)
                        if lineList[0][6] == "0":
                            self.MerkleTreeRoot = MerkleTreeNode(readKey)
                            self.MerkleTreeRoot.left = self.nodeDict[readKey].left
                            self.MerkleTreeRoot.right = self.nodeDict[readKey].right
                    # Exception handler: undefined
                    else:
                        assert False
        else:
            # Do nothing...{} and None
            return


    def printBFS(self) -> list:
        """
            Print the Merkle Tree in BFS order.
        """
        # Initialization: multi-list of BFS 
        BFS_list = []
        # First load the root node into un-parsed queue
        unparsedQueue = deque([self.MerkleTreeRoot.key]) if self.MerkleTreeRoot.key is not None else None
        # Until un-parsed queue is NONE
        while unparsedQueue:
            # Specifically record the elements within each level
            # e.g., [[0],[1,1],[2,2,2,2]]
            levelList = list(unparsedQueue)
            # Update the results of each level
            BFS_list.append(levelList)
            # Prepare to-be-parsed nodes for the next level
            for n in levelList:
                # Pop out the parsed node in queue
                unparsedQueue.popleft()
                # See if the left child is needed
                if self.nodeDict[n].left != None:
                    unparsedQueue.append(self.nodeDict[n].left)
                # See if the right child is needed
                if self.nodeDict[n].right != None:
                    unparsedQueue.append(self.nodeDict[n].right)
        return BFS_list


    def saveMerkleTree_BFS(self, path_tree:str):
        """
            Save existing Merkle Tree into file
        """
        # Prepare the BFS order
        BFS_list = self.printBFS()
        with open(path_tree, mode='w') as filePtr:
            filePtr.write("*** This is for Merkle Tree user-friendly graph in BFS order. *** \n")
            filePtr.write("*** Levels start from Root [0] to leafs [log n] *** \n")
            filePtr.write("*** e.g. Level(n): Hash [key] <left,right>:childs \n")
            # For each level in BFS order
            for i in range(0, len(BFS_list)):
                for j in BFS_list[i]:
                    # Print the leaf nodes: Level(n): {hash} [key]
                    filePtr.write("Level(" + str(i) + "): " + self.nodeDict[j].hash + " [" + j + "]")
                    # Add <left,right>:childs if available
                    if self.nodeDict[j].left != None and self.nodeDict[j].right != None:
                        filePtr.write(" <" + self.nodeDict[j].left + "," + self.nodeDict[j].right + ">")
                    filePtr.write(" \n")


    def getConnection(self) -> dict:
        """
            Get connections of Merkle Tree (in BFS order)
        """
        # Initialization: dictionary {parent: [left,right]}
        MerkleTreeConnect = {}
        # First load the root node into un-parsed queue
        unparsedQueue = deque([self.MerkleTreeRoot.key]) if self.MerkleTreeRoot.key is not None else None
        # Until un-parsed queue is NONE
        while unparsedQueue:
            # Since the tree in this project is rigorously 'balanced'
            # Each node has either 2 (left,right) or 0 nodes
            tmp = unparsedQueue.popleft()
            if self.nodeDict[tmp].left != None and self.nodeDict[tmp].right != None:
                MerkleTreeConnect[tmp] = [self.nodeDict[tmp].left, self.nodeDict[tmp].right]
                unparsedQueue.append(self.nodeDict[tmp].left)
                unparsedQueue.append(self.nodeDict[tmp].right)
        return MerkleTreeConnect


    def getInclusionProof(self, lookup:str) -> list:
        """
            Get the Inclusion Proof #RFC-9162 2.1.3
        """
        # NOT found in Merkle Tree
        if self.nodeDict.get(lookup) == None:
            return []
        # Initialization: the required proof of given lookup
        query = lookup
        inclusionProof = []
        # Get self connection of Merkle Tree
        connect = self.getConnection()
        # Until it reaches the root
        while query != self.MerkleTreeRoot.key:
            # Find query in childs (L or R)
            parent = ""
            childs = [] 
            for k,v in connect.items():
                if query in v:
                    # Found, save then break the loop
                    parent = k
                    childs = list(v)
                    break
            # From the 'left' child to keep the 'right' proof
            if query == childs[0]:
                inclusionProof.append(self.nodeDict[childs[1]].hash)
            # From the 'right' child to keep the 'left' proof
            elif query == childs[1]:
                inclusionProof.append(self.nodeDict[childs[0]].hash)
            # Exception: undefined
            else:
                assert False
            # Next move up to the found's parent
            query = parent
        return inclusionProof


    def getConsistencyProof(self, cmp_tree) -> list:
        """
            Get the Consistency Proof #RFC-9162 2.1.4
        """
        assert cmp_tree.nodeDict != {} and cmp_tree.MerkleTreeRoot.key != None
        # Initialization: the required proof of given tree
        consistencyProof = []
        # Self root is found within the compared Merkle Tree
        if cmp_tree.nodeDict.get(self.MerkleTreeRoot.key) != None:
            consistencyProof.extend(cmp_tree.getInclusionProof(self.MerkleTreeRoot.key))
        # Self root is NOT found (& NOT completed) within the compared Merkle Tree
        else:
            consistencyProof.append(self.nodeDict[self.MerkleTreeRoot.right].hash)
            consistencyProof.extend(cmp_tree.getInclusionProof(self.MerkleTreeRoot.right))
        # Finished and return the answer
        return consistencyProof
