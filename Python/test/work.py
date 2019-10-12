from __future__ import print_function
'''
Created on Apr 11, 2019

@author: NOOK
'''
import sys
from doxypypy import doxypypy
from unittest.mock import patch
from TestData import testDataPath


# some python 2 and 3 comnpatibility tweaks
import sys
py3=sys.version_info >= (3, 0)
def inext(v):  # next value from iterator
    return next(v) if py3 else v.next()

import os
import time
import apsw

###
### Check we have the expected version of apsw and sqlite
###


class NullDevice():
    def __init__(self):
        self.buffer = '';
    def write(self, s):
        self.buffer += s;
    
    def flush(self):
        pass

class FloatingPointDifferences :
    
    def __init__(self):
        path = testDataPath("FloatingPointDifferences.sqlite")
        self.connection=apsw.Connection(path)
        self.cursor = self.connection.cursor()
        
    def create(self) -> None:
        try :
            self.cursor.execute("drop table errors");
        except :
            pass
        self.cursor.execute("create table errors(target TEXT, test TEXT, bits REAL)")
        
    def add(self, target : str, test : str, bits : float) -> None:
        for bits, test in self.cursor.execute("select bits, test from errors WHERE target == ? AND test == ?", (target, test,)):
            self.cursor.execute("update errors set bits=? WHERE target == ? AND test == ?", (bits, target, test,));
            return
        self.cursor.execute("insert into errors(target, test, bits) values(?, ?, ?)", (target, test, bits))
        
    def get(self, target : str, test : str) -> float:
        for bits in self.cursor.execute("select bits from errors WHERE target == ? AND test == ?", (target, test,)):
            return bits
        return None
    
    def dump(self):
        for target, test, bits in self.cursor.execute("select target, test, bits from errors") :
            print(target, test, bits)

if __name__ == '__main__':
    print ("      Using APSW file",apsw.__file__)                # from the extension module
    print ("         APSW version",apsw.apswversion())           # from the extension module
    print ("   SQLite lib version",apsw.sqlitelibversion())      # from the sqlite library code
    print ("SQLite header version",apsw.SQLITE_VERSION_NUMBER)   # from the sqlite header file at compile time
    
    fpDiffs = FloatingPointDifferences()
    fpDiffs.create();
    fpDiffs.add("Cpp/Eigen", "Emp_test/test1CheckVRF", 0);
    fpDiffs.add("Cpp/Eigen", "Emp_test/test1CheckVRF",    0);
    fpDiffs.add("Cpp/Eigen", "Emp_test/test2CheckStates",    19.988151)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckMidpoints/0",    6.937761)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckMidpoints/1",    6.81428)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckMidpoints/10",    5.897989)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckMidpoints/2",    0)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckMidpoints/3",    0)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckMidpoints/4",    0)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckMidpoints/5",    0)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckMidpoints/6",    5.796589)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckMidpoints/7",    5.688149)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckMidpoints/8",    7.546648)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckMidpoints/9",    7.88977)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckNoisy/0",    0)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckNoisy/1",    0)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckNoisy/2",    7.251613)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckNoisy/3",    6.329308)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckNoisy/4",    14.288853)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckNoisy/5",    17.473965)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckPerfect/0",    0)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckPerfect/1",    0)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckPerfect/2",    5.897989)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckPerfect/3",    12.372557)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckPerfect/4",    17.331042)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckPerfect/5",    22.939553)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test1CheckVrfs",    14.928315)
    fpDiffs.add("Cpp/Eigen", "FixedMemoryFilter_test/test9Regresssion",    0)
    fpDiffs.add("Cpp/Eigen", "Fmp_test/test1CheckGammas",    0)
    fpDiffs.add("Cpp/Eigen", "Fmp_test/test1CheckStates",    0)
    fpDiffs.add("Cpp/Eigen", "Fmp_test/test1CheckVrfs",    0)
    fpDiffs.add("Cpp/Eigen", "Fmp_test/test9Basic",    17.31004)
    fpDiffs.add("Cpp/Eigen", "Fmp_test/test9CoreBasic",    0)
    fpDiffs.add("Cpp/Eigen", "Pair_test/test2CheckStates",    27.774999)
    fpDiffs.add("Cpp/Eigen", "RecursivePolynomialFilter_test/test1PureObservation",    16.73)
    fpDiffs.add("Cpp/Eigen", "RecursivePolynomialFilter_test/test1PurePredict",    0)
    fpDiffs.add("Cpp/Eigen", "RecursivePolynomialFilter_test/test9Coverage",    0)
    
    fpDiffs.add("Java/EJML", "Emp_test/test1CheckVRF", 0)
    fpDiffs.add("Java/EJML", "Emp_test/test2CheckStates", 20.36)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckMidpoints/0", 6.85)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckMidpoints/1", 6.3)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckMidpoints/10", 6.68)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckMidpoints/2", 5.81)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckMidpoints/3", 0)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckMidpoints/4", 0)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckMidpoints/5", 0)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckMidpoints/6", 0)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckMidpoints/7", 6.18)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckMidpoints/8", 7.67)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckMidpoints/9", 8.13)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckNoisy/0", 0)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckNoisy/1", 0)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckNoisy/2", 6.26)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckNoisy/3", 11.23)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckNoisy/4", 12.93)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckNoisy/5", 16.57)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckPerfect/0", 0)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckPerfect/1", 0)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckPerfect/2", 6.68)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckPerfect/3", 12.74)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckPerfect/4", 15.36)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckPerfect/5", 22.36)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test1CheckVrfs", 15.06)
    fpDiffs.add("Java/EJML", "FixedMemoryFilter_test/test9Regresssion", 0)
    fpDiffs.add("Java/EJML", "Fmp_test/test1CheckGammas", 0)
    fpDiffs.add("Java/EJML", "Fmp_test/test1CheckStates", 0)
    fpDiffs.add("Java/EJML", "Fmp_test/test1CheckVrfs", 0)
    fpDiffs.add("Java/EJML", "Fmp_test/test9Basic", 17.31)
    fpDiffs.add("Java/EJML", "Fmp_test/test9CoreBasic", 0)
    fpDiffs.add("Java/EJML", "Pair_test/test2CheckStates", 29.01)
    fpDiffs.add("Java/EJML", "RecursivePolynomialFilter_test/test1PureObservation", 16.73)
    fpDiffs.add("Java/EJML", "RecursivePolynomialFilter_test/test1PurePredict", 0)
    fpDiffs.add("Java/EJML", "RecursivePolynomialFilter_test/test9Coverage", 0)
    fpDiffs.dump();
    
#     connection=apsw.Connection("dbfile")
#     cursor=connection.cursor()
#     try :
#         cursor.execute("drop table errors");
#     except :
#         pass
#     cursor.execute("create table errors(target TEXT, test TEXT, bits REAL)")
#     cursor.execute("insert into errors(target, test, bits) values(?, ?, ?)", ("Cpp/Eigen", "Emp_test/test1CheckVRF", 0 ))
#     cursor.execute("insert into errors(target, test, bits) values(?, ?, ?)", ("Cpp/Eigen", "Emp_test/test1CheckVRF", 1 ))
#     for bits, test in cursor.execute("select bits, test from errors WHERE target == ?", ("Cpp/Eigen", )):
# #         print (cursor.getdescription())  # shows column names and declared types
#         print (bits, test)

#     original_stdout = sys.stdout  # keep a reference to STDOUT
#     
#     runargs = ["doxypypy", "-a", "../src/DoxygenTest.py"];
#     sys.argv = runargs
#     dev = NullDevice()  # redirect the real STDOUT
#     sys.stdout = dev;
#     doxypypy.main()
#     sys.stdout = original_stdout
#     print(dev.buffer)