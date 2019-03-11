'''
Created on Feb 1, 2019

@author: NOOK
'''
import csv

from numpy import zeros, array, concatenate, arange, ones, diag, sqrt, transpose,\
    allclose, mean, std
from numpy import array as vector;
from numpy.linalg import cholesky, LinAlgError
from scipy.interpolate import PchipInterpolator
import pymap3d
import xml.etree.ElementTree as ET 
from PolynomialFiltering.Components.ExpandingMemoryPolynomialFilter import makeEMP;
from TestUtilities import A2S, scaleVRFEMP, covarianceToCorrelation, correlationToCovariance;

def readData(): 
    with open('../test/landing.csv', newline='') as csvfile:
        L = csv.DictReader(csvfile)
        tspi = zeros([0,4]);
        for row in L :
            p = array([float(row['time']), float(row['east']), float(row['north']), float(row['up'])]);
            p.shape = (1,4);
            tspi = concatenate([tspi, p],axis=0);
        print(tspi[0,0], tspi[-1,0])
        p = PchipInterpolator(tspi[:,0], tspi[:,1], axis=0)
        t = arange(tspi[0,0], tspi[-1,0]);
        print(p(t))

def isPositiveDefinite( V : array ):
    if (not allclose(transpose(V), V, atol=1e-14)) :
#         print('not PD')
        print(A2S(transpose(V)-V))
        return False;
    try :
        cholesky(V)
        return True;
    except LinAlgError:
#         print('not PD chol')
        return False;
            
    
def scaleVRFEMP( V : array, t : float, n : float ) -> array:
    '''@S : array'''
    '''@i : int'''
    '''@j : int'''
    S = zeros([V.shape[0], V.shape[1]]);
    S[0,0] = 1.0/n;
    for i in range(1,S.shape[0]) :
        S[i,0] = S[i-1,0] / (t*n);
    for i in range(0,S.shape[0]) :
        for j in range(1,S.shape[1]) :
            S[i,j] = S[i,j-1] / (t*n);
    return S * V;

def baseCovarianceToCorrelation( C : array) -> array:
    (K,__) = covarianceToCorrelation(C);
    decl = 'C = array([';
    for i in range(0,K.shape[0]) :
        if (i != 0) :
            decl += ', ';
        decl += '[';
        for j in range(0,K.shape[1]) :
            if (j != 0) :
                decl += ', ';
            decl += ('%.12g' % K[i,j]);
        decl += ']';
    decl += ']);'
    print(decl)
    return K;

def VRF2(order : int):
    u = 0.1;
    emp = makeEMP(order, u)
    C = array([[9,36,60],[36,192,360],[60,360,720]]);
    K = baseCovarianceToCorrelation(C);
    print('large n VRF base std dev')
    print(A2S(K))
    for n in [10, 25, 50, 100, 500, 1000, 5000] :
        print(order, u, n)
        emp.n = n;
        P1 = emp.getCovariance(1)
#         V = scaleVRFEMP(ones([order+1,order+1]), u, n);
#         print('scale diag ', A2S(diag(V)))
#         print('       new ', A2S(scaleDiagEMP(order, u, n)))
# #         print(A2S(V))
#         (VK,Vd) = covarianceToCorrelation(V);
#         print(A2S(VK))
#         print(A2S(Vd))
#         print(A2S(Vd*Vd))
        D = zeros([order+1])
        D[0] = sqrt(3*(3*n**2+9*n+8) / ((n+1)*n*(n-1)));
        D[1] =  sqrt(12*(16*n**2+62*n+57) / (u**2*(n+3)*(n+2)*(n+1)*n*(n-1)));
        D[2] = sqrt(720 / (u**4*(n+3)*(n+2)*(n+1)*n*(n-1)));
        P0 = correlationToCovariance(K, D);
        print('new/old P0', isPositiveDefinite(P0), isPositiveDefinite(P1))
        print(A2S( P0 ))
        print(A2S( P1-P0 ))
        for i in range(-5,+6) :
            F = emp.stateTransitionMatrix(emp.order+1, i);
            V = transpose(F) @ P0 @ F;
            print(i, isPositiveDefinite(V), end='; ')
        print('')
        
    
def loadTrajectory():
    xmlfile = "/Users/NOOK/Google Drive/BlueStick/data/X-37 RWY 12 short.jTraj"
    filename = 'landing.csv'
    # create element tree object 
    tree = ET.parse(xmlfile) 
    root = tree.getroot() 
    
    with open(filename, 'w', newline='') as csvfile: 
        fields = ['time','east','north', 'up', 'azimuth', 'elevation', 'range']
        writer = csv.DictWriter(csvfile, fieldnames = fields) 
        writer.writeheader() 
        sensor = [0.607302876756862, -2.1026663520973794, 100]
        samples = []
        for tspiRow in root :
            t = float(tspiRow.attrib['time'])
            E = float(tspiRow.attrib['E'])
            F = float(tspiRow.attrib['F'])
            G = float(tspiRow.attrib['G'])
            x, y, z = pymap3d.ecef2enu(E, F, G, sensor[0], sensor[1], sensor[2], deg=False)
            z = 0.456*z
            E, F, G = pymap3d.enu2ecef(x, y, z, sensor[0], sensor[1], sensor[2], deg=False)
            a, e, r = pymap3d.ecef2aer(E, F, G, sensor[0], sensor[1], sensor[2], deg=False)
            print(t-1500,x,y,z,a,e,r)
            row = {}
            row[fields[0]] = 2.72*(t-1500)
            row[fields[1]] = x
            row[fields[2]] = y
            row[fields[3]] = z
            row[fields[4]] = a
            row[fields[5]] = e
            row[fields[6]] = r
            samples.append(row)
        writer.writerows(samples)
        
def scaleDiagEMP( order : int, u : float, n : float) -> vector:
    S = zeros([order+1]);
    S[0] = 1.0/n;
    for i in range(1,order+1) :
        S[i] = S[i-1] / ((u*n)*(u*n));
    return S;
    
        
if __name__ == '__main__':
    pass
#     order = 2;
#     u = 1;
#     n = 10;
#     V = scaleVRFEMP(ones([order+1,order+1]), u, n);
#     print('scale diag ', A2S(diag(V)))
#     print('       new ', A2S(scaleDiagEMP(order, u, n)))
#     u = 10;
#     n = 1;
#     V = scaleVRFEMP(ones([order+1,order+1]), u, n);
#     print('scale diag ', A2S(diag(V)))
#     print('       new ', A2S(scaleDiagEMP(order, u, n)))
#     C = array([[4,6],[6,12]]);
#     K = baseCovarianceToCorrelation(C);
#     C = array([[9,36,60],[36,192,360],[60,360,720]]);
#     K = baseCovarianceToCorrelation(C);
#     C = array([[16, 120, 480, 840],[120, 1200,5400, 10080],[480, 5400, 25920, 50400],[840, 10080, 50400, 100800]]);
#     K = baseCovarianceToCorrelation(C);
#     C = array([[25, 300, 2100, 8400, 15120],[300, 4800, 37800, 161280, 302400],[2100, 37800, 317520, 1411200, 2721600],[8400, 161280, 1411200, 6451200, 12700800],[15120, 302400, 2721600, 12700800, 25401600]]);
#     K = baseCovarianceToCorrelation(C);
#     C = array([[36, 630, 6720, 45360, 181440, 332640],[630, 14700, 176400, 1270080, 5292000, 9979200],[6720, 176400, 2257920, 16934400, 72576000, 139708800],[45360, 1270080, 16934400, 130636800, 571536000, 1117670400],[181440, 5292000, 72576000, 571536000, 2540160000, 5029516800],[332640, 9979200, 139708800, 1117670400, 5029516800, 10059033600]]);
#     K = baseCovarianceToCorrelation(C);
    
#     VRF2(2)

#     C = array([[36, 630, 6720, 45360, 181440, 332640],[630, 14700, 176400, 1270080, 5292000, 9979200],[6720, 176400, 2257920, 16934400, 72576000, 139708800],[45360, 1270080, 16934400, 130636800, 571536000, 1117670400],[181440, 5292000, 72576000, 571536000, 2540160000, 5029516800],[332640, 9979200, 139708800, 1117670400, 5029516800, 10059033600]]);
#     print(A2S( scaleVRFEMP( C, 1e-3, 15000-500)) )
#     
#     A = array([10])
#     print(cholesky(A))
    k = -0.5 # /sqrt(3.0)
    n = 1.0
    w0 = k/(n+k)
    wi = 1.0/(2*(n+k))
    s = sqrt(n+k)
    
    A = wi * array([-s, +s])
    print((A @ A.T))
        