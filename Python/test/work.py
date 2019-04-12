'''
Created on Apr 11, 2019

@author: NOOK
'''
import sys
from doxypypy import doxypypy
from unittest.mock import patch

class NullDevice():
    def __init__(self):
        self.buffer = '';
    def write(self, s):
        self.buffer += s;
    
    def flush(self):
        pass


if __name__ == '__main__':
    original_stdout = sys.stdout  # keep a reference to STDOUT
    
    runargs = ["doxypypy", "-a", "../src/DoxygenTest.py"];
    sys.argv = runargs
    dev = NullDevice()  # redirect the real STDOUT
    sys.stdout = dev;
    doxypypy.main()
    sys.stdout = original_stdout
    print(dev.buffer)