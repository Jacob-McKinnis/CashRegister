// To install python 3.12.5 from the command line (on Windows):

// Run the following command: 
Invoke-WebRequest -UseBasicParsing -Uri 'https://www.python.org/ftp/python/3.12.5/python-3.12.5-amd64.exe' -OutFile 'python-3.12.5-amd64.exe'

// This will take a few minutes
// At the end, the file 'python-3.12.5-amd64.exe' will be in the current directory

// Run the following command to silently install this python version for the current user
.\python-3.12.5-amd64.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0

// Wait a few minutes for this to run, then close and re-open the terminal

// Run the following command
python --version

// This should print 'Python 3.12.5'


// Once python is installed, run the file using this command:
python getChange.py -h

// This will list all valid parameters and the types of data they expect

// A few example commands:
python getChange.py -in input.txt

python getChange.py -in input.txt -out output

python getChange.py -in input.txt -out output -c USD

python getChange.py -in input.txt -out output -c EUR