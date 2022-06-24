"""
main.py
====================================
The command-line script for parsing ScratchText and turning it into Scratch Blocks
"""

from pyscratch import parser as scratch_paser
import argparse
import os

os.chdir("../")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compile ScratchText into a .sb3 file.')
    parser.add_argument('filepath', type=str, nargs="*", help='the path to the script to compile')
    parser.add_argument("--print", "-p", dest='print_output', action='store_true')

    args = parser.parse_args()

    if args.filepath:
        result = scratch_paser.parse(args.filepath[0])
        if args.print_output:
            print(result)

    else:  # No args were supplied.
        parser.print_help()
        print("\nIgnore this if you aren't running from CLI.")
        # Insert a custom filepath here:
        filepath = "./script.st"
        print(scratch_paser.parse(filepath))
