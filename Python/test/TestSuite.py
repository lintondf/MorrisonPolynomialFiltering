'''
Created on Mar 27, 2019

@author: NOOK
'''
import os
import unittest
import coverage

def testDataPath( filename : str) -> str:
    path = os.getcwd();
    return path.replace("\\", "/").replace("Python/test.*", "testdata") + filename;

# .. call your code ..

def runAll():
    testmodules = [
        'Components.AbstractRecursiveFilter_test',
        'Components.EMP_test',
        'Components.FixedMemoryFilter_test',
        'Components.FMP_test',
        'Components.EmpFmpPair_test',
        'filters.ManagedFilterBase_test',
        'filters.controls.ConstantObservationErrorModel_test',
        ]
    
    suite = unittest.TestSuite()
    
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
    cov = coverage.Coverage()
    cov.start()
    runAll()
    cov.stop()
    cov.save()
    cov.html_report()
    