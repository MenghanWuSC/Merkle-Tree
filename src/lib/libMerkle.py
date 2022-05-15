

import hashlib

# Class: each node of Merkle Tree
class MerkleTreeNode:
    def __init__(self, key:str, hash:str=None):
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


# Class: a general instance of Merkle Tree
class MerkleTree:
    def __init__(self, nodes:list=None, path_tree:str=None):
        """
            Build a Merkle Tree from given 1) list 2) file.
            Instances: {nodeDict}, MerkleTreeRoot
        """
        self.nodeDict = {}
        self.MerkleTreeRoot = None
        # Constructor 1. initialization by nodes
        if nodes != None and path_tree == None:
            assert len(nodes) > 0
            # Only one node
            if len(nodes) == 1:
                self.nodeDict[nodes[0]] = MerkleTreeNode(nodes[0])
                self.MerkleTreeRoot = self.nodeDict[nodes[0]]
                return
            # More nodes
            # Prepare 'leaf' nodes from given list
            for n in nodes:
                self.nodeDict[n] = MerkleTreeNode(n)
            # Start from at least 2 nodes
            while len(nodes) >= 2:
                parentKey = None
                parentList = []
                # For every 2 first nodes, do the concatenation & hash
                for i in range(1, len(nodes), 2):
                    parentKey = self.nodeDict[nodes[i-1]].hash + self.nodeDict[nodes[i]].hash
                    self.nodeDict[parentKey] = MerkleTreeNode(parentKey)
                    self.nodeDict[parentKey].left = nodes[i-1]
                    self.nodeDict[parentKey].right = nodes[i]
                    # Prepare 'parent' nodes
                    parentList.append(parentKey)
                    # Handle the remaining odd node
                    if i+1 == len(nodes)-1:
                        parentList.append(nodes[i+1])
                        break
                # Renew the loop condition
                nodes = parentList
            # After divided processing by 2 only the root [0] is left
            assert len(nodes) == 1
            self.MerkleTreeRoot = self.nodeDict[nodes[0]]
        # Constructor 2. initialization from file
        elif nodes == None and path_tree != None:
            with open(path_tree, mode='r') as filePtr:
                # For each line in I/O stream
                for line in filePtr:
                    lineList = line.split(" ")
                    # Ignore the comments '***'
                    if lineList[0] == "***":
                        continue
                    # Handle the leaf format: Level(n): Hash [key]
                    elif len(lineList) == 4:
                        readKey = lineList[2][1:len(lineList[2])-1]
                        self.nodeDict[readKey] = MerkleTreeNode(readKey, lineList[1])
                    # Handle the parent format: Level(n): Hash [key] <left,right>:childs
                    elif len(lineList) == 5:
                        readKey = lineList[2][1:len(lineList[2])-1]
                        self.nodeDict[readKey] = MerkleTreeNode(readKey, lineList[1])
                        readLeft = lineList[3][1:lineList[3].find(",")]
                        readRight = lineList[3][lineList[3].find(",")+1:len(lineList[3])-1]
                        self.nodeDict[readKey].left = readLeft
                        self.nodeDict[readKey].right = readRight
                        # Prepare string list of connection
                        # e.g. Connect: key = a + b
                        # ...
                        #tmpString = "Connect: " + readKey + " = " + readLeft + " + " + readRight
                        #MerkleTreeConnect.append(tmpString)
                        # Get the root: Level(0)
                        if lineList[0][6] == "0":
                            self.MerkleTreeRoot = self.nodeDict[readKey]
                    # Exception handler: undefined
                    else:
                        assert False
        else:
            # Parameter conflicts: nodes/path_tree
            raise AttributeError

    def printBFS(self) -> list:
        """
            Print the Merkle Tree in BFS order.
        """
        assert self.MerkleTreeRoot != None
        assert self.nodeDict != None and len(self.nodeDict) > 0
        # Initialization: multi-list of BFS 
        BFS_list = []
        # First load the root node into to-be-parsed list
        parsedList = [self.MerkleTreeRoot.key]
        # Until the parsed list NONE
        while parsedList:
            # Specifically record the elements within each level
            leveltmp = None
            levelSize = len(parsedList)
            levelList = []
            while levelSize > 0:
                # Pop out the parsed list
                leveltmp = parsedList.pop(0)
                levelSize -= 1
                levelList.append(leveltmp)
                # See if the left child is needed
                if self.nodeDict[leveltmp].left != None:
                    parsedList.append(self.nodeDict[leveltmp].left)
                # See if the right child is needed
                if self.nodeDict[leveltmp].right != None:
                    parsedList.append(self.nodeDict[leveltmp].right)
            # Update the results of each level
            BFS_list.append(levelList)
        # Finish the parsing
        return BFS_list

    def saveMerkleTree_BFS(self, path_tree:str):
        """
            Save existing Merkle Tree into file
        """
        # Prepare the BFS order
        BFS_list = self.printBFS()
        assert BFS_list != None and len(BFS_list) > 0
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
        assert self.MerkleTreeRoot != None
        assert self.nodeDict != None and len(self.nodeDict) > 0
        # Initialization: dictionary {'key': [left,right]}
        MerkleTreeConnect = {}
        # First load the root node into to-be-parsed list
        parsedList = [self.MerkleTreeRoot.key]
        # Until the parsed list NONE
        while parsedList:
            # Since the tree in this project is rigorously 'balanced'
            # Each node has either 2 (left,right) or 0 nodes
            tmp = parsedList.pop(0)
            if self.nodeDict[tmp].left != None and self.nodeDict[tmp].right != None:
                MerkleTreeConnect[tmp] = [self.nodeDict[tmp].left, self.nodeDict[tmp].right]
                parsedList.append(self.nodeDict[tmp].left)
                parsedList.append(self.nodeDict[tmp].right)
        # Done
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
            for k,v in connect.items():
                if query in v:
                    # Found (k,v) as the matched 
                    break
            # From 'left' to request 'right'
            if query == v[0]:
                inclusionProof.append(self.nodeDict[v[1]].hash)
            # From 'right' to request 'left'
            elif query == v[1]:
                inclusionProof.append(self.nodeDict[v[0]].hash)
            # Exception: undefined
            else:
                assert False
            # Next move up to the found's parent
            query = k
        # Finished and return the answer
        return inclusionProof

    def getConsistencyProof(self, new_tree) -> list:
        """
            Get the Consistency Proof #RFC-9162 2.1.4
        """
        assert new_tree != None
        # Initialization: the required proof of given tree
        consistencyProof = []
        # Old root is found within the new Merkle Tree
        if new_tree.nodeDict.get(self.MerkleTreeRoot.key) != None:
            consistencyProof.extend(new_tree.getInclusionProof(self.MerkleTreeRoot.key))
        # Old root is NOT found (& NOT completed) within the new Merkle Tree
        else:
            consistencyProof.append(self.nodeDict[self.MerkleTreeRoot.right].hash)
            consistencyProof.extend(new_tree.getInclusionProof(self.MerkleTreeRoot.right))
        # Finished and return the answer
        return consistencyProof
