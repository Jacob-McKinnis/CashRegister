# Author: Jacob McKinnis 
# Last Edited: 08/10/2024

import argparse
import decimal
import os
import random
import sys

# Global variables:
debugMode = False
currencyPrecision = 100
currencyRounding = decimal.ROUND_HALF_DOWN
currencyZero = decimal.Decimal("0")
specialDivisor = "3"

currencyUnits = [
    ["100","100 dollar bill","100 dollar bills"],
    ["20","20 dollar bill","20 dollar bills"],
    ["10","10 dollar bill","10 dollar bills"],
    ["5","5 dollar bill","5 dollar bills"],
    ["1","1 dollar bill","1 dollar bills"],
    ["0.25","quarter","quarters"],
    ["0.1","dime","dimes"],
    ["0.05","nickle","nickles"],
    ["0.01","penny","pennies"],
]

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
    return currency.quantize(decimal.Decimal("0.01"))

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
    
## 1.3 Set up currency handling
# Set the precison (aka number of significant digits) to 100
decimal.getcontext().prec = currencyPrecision
# From https://docs.python.org/3/library/decimal.html#rounding-modes
# "Round to nearest with ties going towards zero."
decimal.getcontext().rounding = currencyRounding
    
# 2. Process input file
f = open(args.file, "r")
output = []
for x in f:
    line = x.rstrip('\r\n')
    debugPrint(f"Line: {line}")
    
    ## 2.1 line text validation
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
    
    ## 2.2 Process line text
    change = paid - owed
    debugPrint(f"Diff: {getCurrencyValue(change)}")
    
    divisor = decimal.Decimal(specialDivisor) * decimal.Decimal("0.01")
    debugPrint(owed % divisor)
    
    changeRemaining = change
    results = []
    
    if owed % divisor == currencyZero:
        debugPrint("Special case")
        
        unitCounts = {}
        for index, unit in enumerate(currencyUnits):
            unitCounts[index] = 0
        
        maxUnitIndex = 0
        while changeRemaining > currencyZero:
            # Choose a unit at random 
            index = random.randint(maxUnitIndex, len(currencyUnits) - 1)
            randUnit = currencyUnits[index]
            unitValue = decimal.Decimal(randUnit[0])
            if unitValue <= changeRemaining:
                # Update the chosen unit's count
                unitCounts[index] += 1
                changeRemaining -= unitValue
                debugPrint(changeRemaining)
            else:
                # Remove the too large unit from the random pool
                maxUnitIndex = index + 1
                debugPrint(f"Removing {randUnit[1]} as a random option")
                debugPrint(maxUnitIndex)
        debugPrint(unitCounts)
        
        for index, unit in enumerate(currencyUnits):
            count = unitCounts[index]
            if count == 1:
                results.append(f"{count} {unit[1]}")
            elif count > 1:
                results.append(f"{count} {unit[2]}")
    else:
        for unit in currencyUnits:
            count = 0
            unitValue = decimal.Decimal(unit[0])
            while unitValue <= changeRemaining:
                count += 1
                changeRemaining -= unitValue
                debugPrint(changeRemaining)
                
            if count == 1:
                results.append(f"{count} {unit[1]}")
            elif count > 1:
                results.append(f"{count} {unit[2]}")
    
    debugPrint(results)
    output.append(",".join(results))
    
    debugPrint("")
f.close() 