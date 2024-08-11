# Author: Jacob McKinnis 
# Last Edited: 08/10/2024

import argparse
import os
import sys

## Functions: 
# A helper function to output debugging information 
def debugPrint(info):
    if debugMode: print(info)

# 1. Setup
## 1.1 Set up permitted arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "-f", 
    "--file",
    type=str, 
    help="The filepath of a flat file containing amounts owed " +
    "and paid seperated by a comma (for example: 2.13,3.00)"
)
parser.add_argument(
    "-d", 
    "--debug",
    action='store_true',
    help="Enable debug mode, which prints debugging information"
)

## 1.2 Validate arguments
args = parser.parse_args()
debugMode = args.debug
debugPrint(f"File: {args.file}")
debugPrint("")

if not os.path.isfile(args.file):
    sys.exit(f"Invalid file: {args.file}")