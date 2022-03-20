# Merkle Tree
Merkle Tree implementation in Python.

## Environment
> Python 3.8.9 (default, Oct 26 2021, 07:25:53) [Clang 13.0.0 (clang-1300.0.29.30)] on darwin

## Programs
There are three progams in this project:
1. buildmtree.py
2. checkinclusion.py
3. checkconsitency.py

### Class: tree node
Each tree node has `key` as query name, `hash` as **SHA-256** of given name, `left` and `right` as its left or right child.
```
self.key = key
self.hash = hashlib.sha256(key.encode('utf-8')).hexdigest()
self.left = None
self.right = None
```

### Data structure
Implementation in this project represents a general **binary tree without balance** according to [RFC 9162](https://datatracker.ietf.org/doc/html/rfc9162#section-2.1): "...do not require the length of the input list to be a power of two...Merkle Tree may thus not be balanced."

Used global data:
- `MerkleTree` denotes the dictionary for key mapping respective tree nodes, space complexity O(n)
- `MerkleTreeRoot` denotes the Root node of Merkle Tree, space complexity O(1)
- `MerkleTreeConnect` denotes the connection relation of Merkle Tree by string list, space complexity O(log'n)
- `MerkleTreeBFS` denotes the BFS order of Merkle Tree by nested lists, space complexity O(n)

### buildmtree.py
To generate Merkle Tree from given command-line arguments, record the content of the tree into file '*merkle.tree*'
- `buildMerkleTree` function to build Merkle Tree with `MerkleTree` `MerkleTreeRoot` using **bottom-up** method.
- `BFS_binaryTree` function to plot BFS order with `MerkleTreeBFS`.
- `drawMerkleTree` function to save Merkle Tree into file '*merkle.tree*' by BFS order.

### checkinclusion.py
To check the **inclusion proof** of Merkle Tree by reading file '*merkle.tree*'. Given the command-line argument, tell if the query name exists and print required hashes for proof.
- `parseMerkleTree` function to prepare Merkle Tree by parsing file '*merkle.tree*'
- `checkInclusion` function to check the query target and locate the **inclusion proof**

Output text stream:
> yes/no, {inclusion proof}, {Root: hash}

Reference: [RFC 9162 - 2.1.5. Example](https://datatracker.ietf.org/doc/html/rfc9162#section-2.1.5)

### checkconsitency.py
At first generate two Merkle Trees from given command-line arguments. Then to check the **consistency proof** of these trees, tell if the former is included in the latter (correct content plus order as well) and print required hashes for proof.
- `checkConsistency` function as the main handler, calling `buildMerkleTree`, `BFS_binaryTree` for data settings; calling `checkSubarray`, `getInclusion` for **consistency proof**.
- `checkSubarray` function to preliminarily check content and order in view of subarray.
- `getInclusion` function to locate the **consistency proof**

Output text stream:
> yes/no, {older Root: hash}, {consistency proof}, {newer Root: hash}

Reference: [RFC 9162 - 2.1.5. Example](https://datatracker.ietf.org/doc/html/rfc9162#section-2.1.5)
## Test
...
