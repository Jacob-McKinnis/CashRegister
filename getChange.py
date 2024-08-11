# Author: Jacob McKinnis 
# Last Edited: 08/10/2024

import argparse
import decimal
import os
import sys

# Global variables:
debugMode = False

## Functions: 
# A helper function to output debugging information 
def debugPrint(info):
    if debugMode: print(info)
    
# A helper function to safely quit on error, handling file closing as needed
def errorQuit(error: str, file = None):
    if file is not None:
        file.close() 
    sys.exit(error)
    
# A helper function to output currency values
def getCurrencyValue(currency):
    return currency.quantize("0.01")

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
        
    debugPrint(f"Owed: {getCurrencyValue(owed)}")
    debugPrint(f"Paid: {getCurrencyValue(paid)}")
    
    if paid < owed:
        errorQuit(f"Invalid values: paid amount {paid} is less than owed amount {owed}", f)
    
    change = paid - owed
    
    debugPrint(f"Diff: {getCurrencyValue(change)}")
    
    divisor = decimal.Decimal("3") * "0.01"
    debugPrint(owed % divisor)
    
    debugPrint("")
f.close() 