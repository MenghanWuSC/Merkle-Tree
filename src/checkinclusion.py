#!/usr/bin/python3

import sys, argparse
# == Self module ==
import lib.libMerkle


if __name__ == "__main__":
    
    # Initialization: argparse
    parser = argparse.ArgumentParser()
    # Create a required group
    parser.add_argument("inputQuery", help="# subject to be queried", type=str)
    # Convert argument strings to objects
    args = parser.parse_args()

    try:
        # 1. To load the existing Merkle Tree
        a_tree = lib.libMerkle.MerkleTree(initial="merkle.tree")
        # 2. To get the Inclusion Proof
        inclusionProof = a_tree.getInclusionProof(args.inputQuery)
        # *For this project: print additional 'root' hash for proof
        if len(inclusionProof) > 0:
            print("yes", inclusionProof, "Root:["+ a_tree.MerkleTreeRoot.hash +"]")
        else:
            print("no")
    except Exception as e:
        print(type(e), e)
        parser.print_usage()
        sys.exit(9)
