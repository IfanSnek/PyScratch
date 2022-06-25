"""
main.py
====================================
The command-line script for parsing ScratchText and turning it into Scratch Blocks
"""

from pyscratch import parser as scratch_paser
import argparse

def cli():
    parser = argparse.ArgumentParser(description='Compile ScratchText into a .sb3 file.')
    parser.add_argument('filepath', type=str, nargs=1, help='the path to the script to compile')
    parser.add_argument("--print", "-p", dest='print_output', action='store_true', help="Print all unstacked blocks ("
                                                                                        "for debugging).")

    args = parser.parse_args()

    if args.filepath:
        result = scratch_paser.parse(args.filepath[0])
        if args.print_output:
            print(result)
