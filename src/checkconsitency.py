#!/usr/bin/python3

import sys, os, argparse
# == Self module ==
import lib.libMerkle


def checkSubarray(treeNodes1:list, treeNodes2:list) -> bool:
    """
        Preliminarily check two sets if one is another's rigorous subset.
    """
    # Divide given lists by length
    list_long = list(treeNodes1) if len(treeNodes1) > len(treeNodes2) else list(treeNodes2)
    list_short = list(treeNodes2) if len(treeNodes1) > len(treeNodes2) else list(treeNodes1)
    verified = 0
    # Consider the shorter length
    for index_short in range(0, len(list_short)):
        # Verify the order of elements from head to the shorter's tail
        if list_short[index_short] != list_long[index_short]:
            return False
        else:
            verified += 1
    # Pass if verified number is satisfied
    if verified == len(list_short):
        return True
    # Default: shall return 'False'
    return False
# ENDOF: checkSubarray()


if __name__ == "__main__":
    # Initialization: argparse
    parser = argparse.ArgumentParser()
    # Create required groups
    parser.add_argument("inputList_old", help="# Old list of inputs", type=str)
    parser.add_argument("inputList_new", help="# New list of inputs", type=str)
    # Convert argument strings to objects
    args = parser.parse_args()
    # Parse tree nodes from given input strings
    treeNodes_old = args.inputList_old[1:len(args.inputList_old)-1].split(",")
    treeNodes_new = args.inputList_new[1:len(args.inputList_new)-1].split(",")

    try:
        # 1. To build two Merkle Trees
        a_tree = lib.libMerkle.MerkleTree(initial=treeNodes_old)
        b_tree = lib.libMerkle.MerkleTree(initial=treeNodes_new)
        # 2. To save the derived results
        a_tree.saveMerkleTree_BFS("a_merkle.tree")
        b_tree.saveMerkleTree_BFS("b_merkle.tree")
        # *For this project: combine results into "merkle.trees"
        filenames = ["a_merkle.tree", "b_merkle.tree"]
        with open("merkle.trees", mode='w') as writePtr:
            for fname in filenames:
                with open(fname, mode='r') as readPtr:
                    writePtr.write(readPtr.read())
                writePtr.write("-\n")
                os.remove(fname)  
        # 3. Pre-check the order
        if not checkSubarray(treeNodes_old, treeNodes_new):
            print("no")
            sys.exit(1)
        # 4. To get the Consistency Proof
        consistencyProof = a_tree.getConsistencyProof(b_tree)
        print(f"yes olderRoot:[{a_tree.MerkleTreeRoot.hash}] {consistencyProof} newerRoot:[{b_tree.MerkleTreeRoot.hash}]")
    except Exception as e:
        print(type(e), e)
        parser.print_usage()
        sys.exit(9)
