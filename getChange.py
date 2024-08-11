'''Get Change: A script to calculate the amount of change owed in cash transactions'''
# Author: Jacob McKinnis 
# Last Edited: 08/11/2024

import argparse
import decimal
import math
import os
import random
import re
import sys

# Global variables:
debugMode = False
currencyPrecision = 100
currencyRounding = decimal.ROUND_HALF_DOWN
currencyZero = decimal.Decimal("0")
specialDivisor = "3"
outFileCharactersAllowed = "Only alphanumeric and underscore characters allowed."

class CurrencyUnit:
    '''A unit of currency (i.e. a dollar bill)'''
    def __init__(self, value: str, name: str, pluralName: str):
        self.name = name
        self.pluralName = pluralName
        self.value = decimal.Decimal(value)

class Currency:
    '''A type of currency (i.e. the Euro or US Dollar)'''
    def __init__(self, code, unitList: list[list[str]]):
        ''' 
        code: The currency's ISO 4217 currency code \n
        unitList: A list of lists of values to populate CurrencyUnits. \n
        '''
        self.code = code
        
        units: list[CurrencyUnit] = []
        
        # Parse the list of units
        for unit in unitList:
            units.append(CurrencyUnit(unit[0], unit[1], unit[2]))
            
        # Sort the list of units
        units.sort(key=lambda x: x.value, reverse=True)
        
        self.units = units
        self.minorUnit = units[-1].value

currencyOptions = {}        
currencyOptions["USD"] = Currency("USD", [
    ["100","hundred dollar bill","hundred dollar bills"],
    ["50","fifty dollar bill","fifty dollar bills"],
    ["20","twenty dollar bill","twenty dollar bills"],
    ["10","ten dollar bill","ten dollar bills"],
    ["5","five dollar bill","five dollar bills"],
    ["1","one dollar bill","one dollar bills"],
    ["0.25","quarter","quarters"],
    ["0.1","dime","dimes"],
    ["0.05","nickle","nickles"],
    ["0.01","penny","pennies"],
])
currencyOptions["EUR"] = Currency("EUR", [
    ["500","five hundred euro note","five hundred euro notes"],
    ["200","two hundred euro note","two hundred euro notes"],
    ["100","hundred euro note","hundred euro notes"],
    ["50","fifty euro note","fifty euro notes"],
    ["20","twenty euro note","twenty euro notes"],
    ["10","ten euro note","ten euro notes"],
    ["5","five euro note","five euro notes"],
    ["2","two euro coin","two euro coins"],
    ["1","one euro coin","one euro coins"],
    ["0.50","fifty euro cent coin","fifty euro cent coins"],
    ["0.20","twenty euro cent coin","twenty euro cent coins"],
    ["0.10","ten euro cent coin","ten euro cent coins"],
    ["0.05","five euro cent coin","five euro cent coins"],
    ["0.02","two euro cent coin","two euro cent coins"],
    ["0.01","one euro cent coin","one euro cent coins"],
])
defaultCurrency = "USD"
selectedCurrency = currencyOptions[defaultCurrency]

## Functions: 
def debugPrint(info):
    '''A helper function to output debugging information '''
    if debugMode: print(info)
    
def errorQuit(error: str, file = None):
    '''A helper function to safely quit on error, handling file closing as needed'''
    if file is not None:
        file.close() 
    sys.exit(error)
    
# 
def getCurrencyValue(currency):
    '''A helper function to output currency values'''
    return currency.quantize(selectedCurrency.minorUnit)

# 1. Setup
## 1.1 Set up permitted arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "-in", 
    "--inputFile",
    "--input",
    type=str, 
    help="The filepath of a flat file containing amounts owed " +
    "and paid seperated by a comma (for example: 2.13,3.00)"
)
parser.add_argument(
    "-out", 
    "--outputFilename",
    "--outFile",
    "--output",
    type=str, 
    default="change_output",
    help=f"The filename for the output file. {outFileCharactersAllowed}"
)
parser.add_argument(
    "-c", 
    "--currencyCode",
    "--code",
    type=str, 
    default="USD",
    help=f"The ISO 4217 currency code for the chosen currency. " +
    f"Current options: {",".join(list(currencyOptions.keys()))}"
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
debugPrint(f"File: {args.inputFile}")
selectedCurrency = currencyOptions[args.currencyCode]
debugPrint(f"Currency: {selectedCurrency.code}")
debugPrint(f"Out File: {selectedCurrency.code}")
debugPrint("")

if not os.path.isfile(args.inputFile):
    errorQuit(f"Invalid input file: '{args.inputFile}'")
    
if re.match('^[a-zA-Z0-9_]+$', args.outputFilename) is None:
    errorQuit(f"Invalid output filename: '{args.outputFilename}'. {outFileCharactersAllowed}")

## 1.3 Set up currency handling
# Set the precison (aka number of significant digits) to 100
decimal.getcontext().prec = currencyPrecision
# From https://docs.python.org/3/library/decimal.html#rounding-modes
# "Round to nearest with ties going towards zero."
decimal.getcontext().rounding = currencyRounding

# 2. Process input file
f = open(args.inputFile, "r")
output = []
for x in f:
    line = x.rstrip('\r\n')
    debugPrint(f"Line: {line}")
    
    ## 2.1 Line text validation
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
        
    if not math.isfinite(owed) or not math.isfinite(paid):
        errorQuit(f"Invalid values: unable to convert values in '{line}' to currency", f)
        
    if owed < currencyZero or paid < currencyZero:
        errorQuit(f"Invalid values: negative values in '{line}' not allowed", f)
        
    if owed < selectedCurrency.minorUnit or paid < selectedCurrency.minorUnit:
        errorQuit(f"Invalid values: values in '{line}' too small", f)

    debugPrint(f"Owed: {getCurrencyValue(owed)}")
    debugPrint(f"Paid: {getCurrencyValue(paid)}")
    
    if paid < owed:
        errorQuit(f"Invalid values: paid amount {paid} is less than owed amount {owed}", f)
    
    ## 2.2 Process line text
    change = paid - owed
    debugPrint(f"Diff: {getCurrencyValue(change)}")
    
    divisor = decimal.Decimal(specialDivisor) * selectedCurrency.minorUnit
    debugPrint(owed % divisor)
    
    changeRemaining = change
    results = []
    
    if owed % divisor == currencyZero:
        ## 2.3 Special case processing 
        debugPrint("Special case")
        
        unitCounts = {}
        ### 2.3.1 Initialize a structure to track counts of currency units 
        for index, unit in enumerate(selectedCurrency.units):
            unitCounts[index] = 0
            
        maxUnitIndex = 0
        ### 2.3.2 Generate a random list of valid units 
        while changeRemaining > currencyZero:
            # Choose a unit at random 
            index = random.randint(maxUnitIndex, len(selectedCurrency.units) - 1)
            randUnit = selectedCurrency.units[index]
            
            if randUnit.value <= changeRemaining:
                # Update the chosen unit's count
                unitCounts[index] += 1
                changeRemaining -= randUnit.value
                debugPrint(changeRemaining)
            else:
                # Remove the too large unit from the random pool
                maxUnitIndex = index + 1
                debugPrint(f"Removing {randUnit.name} as a random option")
        
        ### 2.3.3 Create the unit count strings for the output file
        for index, unit in enumerate(selectedCurrency.units):
            count = unitCounts[index]
            if count == 1:
                results.append(f"{count} {unit.name}")
            elif count > 1:
                results.append(f"{count} {unit.pluralName}")
    else:
        ## 2.4 Base case processing 
        for unit in selectedCurrency.units:
            count = 0
            ### 2.4.1 Find the amount of the current unit to be given as change
            while unit.value <= changeRemaining:
                count += 1
                changeRemaining -= unit.value
                debugPrint(changeRemaining)
                
            ### 2.4.2 Create this unit's count string for the output file
            if count == 1:
                results.append(f"{count} {unit.name}")
            elif count > 1:
                results.append(f"{count} {unit.pluralName}")
    
    ## 2.5 Create the result string for the output file and close the input file
    debugPrint(results)
    output.append(",".join(results))
    debugPrint("")
f.close() 

# 3. Write output file
if len(output) > 0:
    outputFilename = f"{args.outputFilename}.txt"
    try: 
        fOut = open(outputFilename, "w")
        fOut.writelines("\n".join(output))
        fOut.close()
    except:
        debugPrint("Output file error: unable to create output file")
    
