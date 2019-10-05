'''
Created on Mar 27, 2019

@author: NOOK
'''
import os
import unittest
import coverage

from time import perf_counter

from unittest import TestCase

class TestCaseBase(TestCase):
    
    def _steps(self):
        for name in dir(self): # dir() result is implicitly sorted
            if name.startswith("step"):
                    yield name, getattr(self, name) 
        
    def test_steps(self):
        if (type(self).__name__ != 'TestCaseBase') :
            print(type(self).__name__)
        for name, step in self._steps():
            try:
                with self.subTest(name):
                    print('  %-50s : ' % name, end='')
                    start = perf_counter()
                    step()
                    print(' OK   %10.6f s' % (perf_counter() - start))
            except Exception as e:
                print(' FAIL %10.6f s' % (perf_counter() - start))
                self.fail("{} failed ({}: {})".format(step, type(e), e))
           
    
def slow() -> bool:
    return True;

def testDataPath( filename : str) -> str:
    path = os.getcwd();
    path = path.replace("\\", "/")
    i = path.find("Python/test")
    path = path[0:i] + "testdata/"
    return path + filename;

# .. call your code ..

def runAll():
    testmodules = [
        'components.AbstractRecursiveFilter_test',
        'components.EMP_test',
        'components.FixedMemoryFilter_test',
        'components.FMP_test',
        'filters.ManagedFilterBase_test',
        'filters.controls.ObservationErrorModel_test',
        ]
    
    suite = unittest.TestSuite()
    
    path = os.getcwd();
    print(path)
    for t in testmodules:
        try:
            # If the module defines a suite() function, call it to get the suite.
            mod = __import__(t, globals(), locals(), ['suite'])
            suitefn = getattr(mod, 'suite')
            suite.addTest(suitefn())
        except (ImportError, AttributeError):
            # else, just load all the test cases from the module.
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))
    
    unittest.TextTestRunner().run(suite)    

if __name__ == '__main__':
#     path = os.getcwd();
#     path = path.replace("\\", "/")
#     i = path.find("Python/test")
#     path = path[0:i] + "/testdata/"
#     print(path)
# cov = coverage.coverage(omit='/usr/lib/python2.6/site-packages/*')
    cov = coverage.Coverage()
    cov.start()
    runAll()
    cov.stop()
    cov.save()
    cov.html_report()
     