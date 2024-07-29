import ROOT
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Print branch names from a ROOT Tree.")
parser.add_argument("file_name", help="Path to the ROOT file")
parser.add_argument("tree_name", help="Name of the tree in the ROOT file")

# Parse arguments
args = parser.parse_args()

# Open the ROOT file
file = ROOT.TFile(args.file_name)

# Access the tree
tree = file.Get(args.tree_name)

# Print the branch names
for branch in tree.GetListOfBranches():
    print(branch.GetName())