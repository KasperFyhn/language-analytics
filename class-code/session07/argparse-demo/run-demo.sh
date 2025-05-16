#!/bin/bash
# Example shell commands to demonstrate the argparse script
# This script pauses between each example for classroom demonstration

pause() {
  echo -e "\nPress Enter to continue to the next example..."
  read
  echo -e "\n----------------------------------------------------"
}

echo "Basic usage with just the required positional argument:"
python main.py input.txt
pause

echo "Using the verbose flag:"
python main.py input.txt --verbose
pause

echo "Using the verbose flag (short form):"
python main.py input.txt -v
pause

echo "Specifying a number:"
python main.py input.txt --number 42
pause

echo "Using a choice argument:"
python main.py input.txt --color blue
pause

echo "Using a wrong choice argument:"
python main.py input.txt --color cyan
pause

echo "Providing multiple values to an argument:"
python main.py input.txt --items apple banana cherry
pause

echo "Specifying an output file:"
python main.py input.txt --output result.txt
pause

echo "Using incremental debug levels:"
python main.py input.txt -d
echo -e "\nWith two debug flags:"
python main.py input.txt -dd
echo -e "\nWith three debug flags:"
python main.py input.txt -ddd
pause

echo "Combining multiple arguments:"
python main.py input.txt -v --number 25 --color green --items cat dog --output out.txt -dd
pause

echo "Show help message:"
python main.py --help
pause

echo "What happens with invalid arguments:"
python main.py input.txt --color purple
pause

echo "What happens when missing required arguments:"
python main.py
pause

echo "Demo complete!"