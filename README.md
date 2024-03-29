# Merkle Tree
Merkle Tree implementation in Python.

## Environment
> Python 3.9.6 (default, Mar 10 2023, 20:16:38) [Clang 14.0.3 (clang-1403.0.22.14.1)] on darwin

## Programs
There are three programs in this project:
1. buildmtree.py
2. checkinclusion.py
3. checkconsitency.py

Implementation in this project represents a general **binary tree without balance** according to [RFC 9162](https://datatracker.ietf.org/doc/html/rfc9162#section-2.1): "...do not require the length of the input list to be a power of two...Merkle Tree may thus not be balanced."

### Class: MerkleTreeNode
Each tree node has `key` as query name, `hash` as **SHA-256** of given name, `left` and `right` as its left or right child.
```
self.key = key
self.hash = hashlib.sha256(key.encode('utf-8')).hexdigest()
self.left = None
self.right = None
```

### Class: MerkleTree
A Merkle tree comprises the data structure `dict` for a key mapping its respective tree node, and the Root node of Merkle Tree.
```
self.nodeDict = {}
self.MerkleTreeRoot = MerkleTreeNode()
```

Class methods:
- `printBFS` return the tree presentation in BFS oreder.
- `saveMerkleTree_BFS` outputs the sample tree view into a storage file.
- `getConnection` returns the connection relation of Merkle Tree by `dict` {parent: [left,right]}
- `getInclusionProof` return the **inclusion proof**
- `getConsistencyProof` return the **consistency proof**

### buildmtree.py
To generate Merkle Tree from given command-line arguments, record the content of the tree into file '*merkle.tree*'.

### checkinclusion.py
To check the **inclusion proof** of Merkle Tree by reading file '*merkle.tree*'. Given the command-line argument, tell if the query name exists and print required hashes for proof.

Output text stream:
> yes/no, {inclusion proof}, {Root: hash}

Reference: [RFC 9162 - 2.1.5. Example](https://datatracker.ietf.org/doc/html/rfc9162#section-2.1.5)

### checkconsitency.py
At first generate two Merkle Trees from given command-line arguments. Then to check the **consistency proof** of these trees, tell if the former is included in the latter (correct content plus order as well) and print required hashes for proof.
- `checkSubarray` function to preliminarily check content and order in view of subarray

Output text stream:
> yes/no, {older Root: hash}, {consistency proof}, {newer Root: hash}

Reference: [RFC 9162 - 2.1.5. Example](https://datatracker.ietf.org/doc/html/rfc9162#section-2.1.5)

## Test

### buildmtree.py
Since this implementation of Merkle Tree **NOT balanced**, the number of leaf nodes **equals** given command-line arguments.
To be noted, the record file reads in **BFS order** from Root (level=0) to leafs (level=log'n).

e.g. Level(n): Hash [key] <left,right>:childs
```
./buildmtree.py [alice,bob,carlol,david]
cat merkle.tree
```
![buildmtree](/img/buildmtree.png)

### checkinclusion.py
Consider a Merkle Tree:[alice,bob,carlol,david] and the query name 'david':
- H(david) = 07d046d5fac12b3f82daf5035b9aae86db5adc8275ebfbf05ec83005a4a8ba3e
- **Inclusion Proof** = [H(carlol), H{alice & bob}] = [5d9896af338ff832d279efd9fac6694c77118a8a5c42425dac1827ea41f97e2a, 92bb1b1e2b4fe6055b9acef6b11b355bf0c58f15aa7b1cde6e3dabec49d95174]
- Root.hash = 0241d53ad33e6e6ae115fdd957c7d09003471d422f18d2a7e9bffcb23a3d9e9a

1. Derive H{carlol & david} = H(H(carlol) || H(david)) = deab4c2ec0d3420cb4064a3043150d5ae7028b71a490f35e34c2a099e1bc2f23
2. Root.hash = H(H{alice & bob} || H{carlol & david}) = 0241d53ad33e6e6ae115fdd957c7d09003471d422f18d2a7e9bffcb23a3d9e9a that **passed**

```
./checkinclusion.py richard
./checkinclusion.py david
```
![checkinclusion](/img/checkinclusion.png)

### checkconsitency.py
Consider two Merkle Trees:[alice,bob,carlol,david] & [alice,bob,carlol,david,eve,fred]:
- Older Root.hash = 0241d53ad33e6e6ae115fdd957c7d09003471d422f18d2a7e9bffcb23a3d9e9a
- **Consistency proof** = [H(H(eve) || H(fred))] = 51ef3f857b1e1c0d59b4150ff4aba5137fdbbd32cba7a3fcb6495408bcb79aa7
- Newer Root.hash = 5a6a6a6bf0dfbf17fab32429ae8e2590af5b71fb09039b3668960d7e31c2c623
1. In this case the older Merkle Tree is **fully balanced**--which means its Root hash should be stored in one of the newer Merkle Tree's parent nodes **needless to re-construct hashes for proof**.
2. Newer Root.hash = H( (olderRoot.hash) || (consistencyProof) ) = 5a6a6a6bf0dfbf17fab32429ae8e2590af5b71fb09039b3668960d7e31c2c623 that **passed**
```
./checkconsitency.py [alice,bob,carlol,david] [alice,bob,carlol,david,eve,fred]
cat merkle.trees
./checkconsitency.py [alice,bob,carlol,david] [alice,bob,david,eve,fred]
cat merkle.trees
./checkconsitency.py [alice,bob,carlol,david] [alice,bob,carol,eve,fred,davis]
cat merkle.trees
```
![checkconsitency_01](/img/checkconsitency_01.png)
![checkconsitency_02](/img/checkconsitency_02.png)
![checkconsitency_03](/img/checkconsitency_03.png)
