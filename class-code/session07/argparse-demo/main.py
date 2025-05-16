#!/usr/bin/env python3
"""
Simple argparse demonstration showing different argument types and styles
"""

import argparse
import sys


def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(
        description='Demo of various argparse argument styles'
    )

    # Positional arguments
    parser.add_argument('filename', help='A positional argument (required)')

    # Optional arguments with different styles

    # Simple flag (store_true)
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='A flag argument (true if present)')

    # Optional argument that requires a value
    parser.add_argument('-n', '--number', type=int, default=10,
                        help='An integer argument with default value')

    # Argument with choices
    parser.add_argument('--color', choices=['red', 'green', 'blue'],
                        help='An argument with specific choices')

    # Argument that can have multiple values
    parser.add_argument('--items', nargs='+',
                        help='An argument that accepts multiple values')

    # Optional argument with different name than dest
    parser.add_argument('-o', '--output', dest='output_file',
                        help='Store value in different variable name')

    # Count argument (-ddd becomes 3)
    parser.add_argument('-d', '--debug', action='count', default=0,
                        help='Increment counter (more -d = higher value)')

    # Parse the arguments
    args = parser.parse_args()

    print("These are the raw inputs from the command line:")
    print(sys.argv)
    print()

    # Show what was received
    print("-- Argument values received with argparse --")
    print(f"filename: {args.filename}")
    print(f"verbose: {args.verbose}")
    print(f"number: {args.number}")
    print(f"color: {args.color}")
    print(f"items: {args.items}")
    print(f"output_file: {args.output_file}")
    print(f"debug level: {args.debug}")


if __name__ == "__main__":
    main()