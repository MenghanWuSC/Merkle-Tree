#!/usr/bin/python3

import sys, argparse
# == Self module ==
import lib.libMerkle


if __name__ == "__main__":
    
    # Initialization: argparse
    parser = argparse.ArgumentParser()
    # Create a required group
    parser.add_argument("inputList", help="# list of inputs", type=str)
    # Convert argument strings to objects
    args = parser.parse_args()
    # Parse tree nodes from given input string
    treeNodes = args.inputList[1:len(args.inputList)-1].split(",")

    try:
        # 1. To build a Merkle Tree
        a_tree = lib.libMerkle.MerkleTree(initial=treeNodes)
        # 2. To save the derived results
        a_tree.saveMerkleTree_BFS("merkle.tree")
    except Exception as e:
        print(type(e), e)
        parser.print_usage()
        sys.exit(9)
