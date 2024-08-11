# Author: Jacob McKinnis 
# Last Edited: 08/10/2024

import argparse
import decimal
import os
import sys

## Functions: 
# A helper function to output debugging information 
def debugPrint(info):
    if debugMode: print(info)
    
def errorQuit(error: str, file = None):
    if file is not None:
        file.close() 
    sys.exit(error)

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
    errorQuit(f"Invalid file: {args.file}")
    
# 2. Process input file
f = open(args.file, "r")
output = []
for x in f:
    line = x.rstrip('\r\n')
    debugPrint(f"Line: {line}")
    
    if "," not in line:
        errorQuit(f"Invalid file formatting: '{line}' does not have a comma", f)
        
    parts = line.split(",")
    debugPrint(f"Parts: {parts}")
    
    if len(parts) != 2:
        errorQuit(f"Invalid file formatting: '{line}' does not have two values", f)
        
    try:
        owed = decimal.Decimal(parts[0])
        paid = decimal.Decimal(parts[1])
    except:
        errorQuit(f"Invalid values: unable to convert values in '{line}' to currency", f)
        
    debugPrint(f"Owed: {owed}")
    debugPrint(f"Paid: {paid}")
    
    debugPrint("")
f.close() 