"""
Jupyter notebook could be good for educational purpose.
Before release in class, output generated during testing and execution number need to be removed.
Some people already wrote some scripts but have problem dealing with special characters  
"""

import os
import sys

import nbformat

if __name__ == '__main__':

    def main(argv):
        if 1 < len(argv):
            filename = argv[1]
            print(filename, os.path.exists(filename))
        else:
            print("Usage : python %s <notebook file path>" % os.path.split(__file__)[-1])
            help(nbformat)


    main(sys.argv)
