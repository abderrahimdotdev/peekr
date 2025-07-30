#!/usr/bin/env python


    
import getopt
import sys


def extract_cli_args():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "hIcrd:k:l:L:o:", ["directory=", "keyword=", "case-sensitive", "interactive","recursive" ,"lang=", "output=", "ui-lang="])
        if len(opts) == 0:
            print_help()
            sys.exit(0)
        else:
            return opts
    except getopt.GetoptError:
        print("Invalid usage.",file = sys.stderr)
        print_help()
        sys.exit(1)

def print_help():
    print("""
    Search text in multiple images using tesseract (an OCR — Optical Character Recognition — tool powered by Google.

    Usage:
        peekr.py [options]

    Options:
        -h, --help  display this help
        -I, --interactive   Run in interactive mode
        -d, --directory Specify the target directory to be searched
        -c, --case-sensitive  Perform a case-sensitive search
        -L, --lang  Specify the language to be used in search (Default is English)
        -l, --ui-lang Specify the language to use when displaying messages
        -r, --recursive Recursively search subdirectories
        -o, --output    Create a folder in the specified location and copy the pictures found into it  
        -k, --keyword A keyword to search for 
    """)
            
def main():
    print_help()


if __name__ == "__main__":
    main()
