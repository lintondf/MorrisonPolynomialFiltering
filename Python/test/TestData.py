'''
Created on Feb 1, 2019

@author: NOOK
'''
import csv

from numpy import zeros, array, concatenate, arange, ones, diag, sqrt, transpose,\
    allclose, mean, std, eye, cov, var, sum
from numpy import array as vector;
from numpy.linalg import cholesky, inv, LinAlgError, det
from scipy.interpolate import PchipInterpolator
import pymap3d
import xml.etree.ElementTree as ET 
from PolynomialFiltering.Main import FilterStatus, AbstractFilter
from PolynomialFiltering.Components.ExpandingMemoryPolynomialFilter import makeEMP
from PolynomialFiltering.Components.FadingMemoryPolynomialFilter import makeFMP
from TestUtilities import A2S, scaleVRFEMP, covarianceToCorrelation, correlationToCovariance, generateTestData, hellingerDistance
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from numpy.random.mtrand import seed
from numpy.random import multivariate_normal

from PolynomialFiltering.PythonUtilities import fdistCdf, fdistPpf, chi2Cdf,\
    chi2Ppf
from numpy.matlib import randn
from PolynomialFiltering.Main import AbstractFilter

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
    K = inv(K)
    decl = 'J = array([';
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

def FMPVRFCorrelations():
    V1 = array([[1.25,    0.5],[0.5,    0.25]]);
    V2 = array([[2.0625,1.6875,0.5],
                [1.6875,    1.75,    0.5625],
                [0.5,    0.5625,    0.1875]]);
    V3 = array([[2.90625,    3.625,    2.15625,    0.5],\
               [3.625,    5.78125,    3.75,    0.90625],\
               [2.15625,    3.75,    2.53125,    0.625],\
               [0.5,    0.90625,    0.625,    0.15625]]);
    
    V4 = array([[3.7695313,   6.3476563,   5.6835938,   2.6367188,   0.5],\
               [6.3476563,   13.75,   13.476563,   6.53125,   1.2695313],\
               [5.6835938,   13.476563,   13.78125,   6.8359375,   1.3476563],\
               [2.6367188,   6.53125,   6.8359375,   3.4375,   0.68359375],\
               [0.5,   1.2695313,   1.3476563,   0.68359375,   0.13671875]]);
    V5 = array([[4.6464844,   9.8789063,   11.832031,   8.2382813,   3.1230469,   0.5],\
               [9.8789063,   27.138672,   35.683594,   26.003906,   10.117188,   1.6464844],\
               [11.832031,   35.683594,   49.054687,   36.640625,   14.472656,   2.3789063],\
               [8.2382813,   26.003906,   36.640625,   27.773438,   11.074219,   1.8320313],\
               [3.1230469,   10.117188,   14.472656,   11.074219,   4.4433594,   0.73828125],\
               [0.5,   1.6464844,   2.3789063,   1.8320313,   0.73828125,   0.12304688]]);
    K = baseCovarianceToCorrelation(V5);
#     print(A2S(K))
    K = baseCovarianceToCorrelation(V4);
#     print(A2S(K))
    K = baseCovarianceToCorrelation(V3);
#     print(A2S(K))
    K = baseCovarianceToCorrelation(V2);
#     print(A2S(K))
    K = baseCovarianceToCorrelation(V1);
#     print(A2S(K))
'''
'''

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
        P1 = emp.getVRF()
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
    
def testEMPSet(Leff : int, pSwitch : float) :
    tau = 0.1
    N = 2500;
    R = 10;
    w = 1 - 2/Leff
    L = int(2.0 / (1.0-w)) # effective length [Morrison1969, Table 13.4]
    order = 3;
    (times, truth, observations, noise) = \
        generateTestData(order, N, 0.0, array([1000, -100, 50, -15, 25, -50]), tau, sigma=sqrt(R))
    
    BET = zeros([N,order+1]);
    emps = [];
    for o in range(0, 5+1) :
        emps.append( makeEMP(o, tau) );
    K = len(emps);
    Z = zeros(order+1);
    for emp in emps :
        emp.start(0, Z);
        
    actual = zeros([N,K]);
    GOFs = 1.959964**2+zeros([N,K]);  # 95% value for normal distribution
    SSRs = zeros([N,K]);
#     Innovations = zeros([N,K]);
    Best = zeros(N, int);
    # actual[0,:] = truth[0,0]
    gofThresholds = zeros([L+1]);
    for i in range(0,L+1) :
        gofThresholds[i] = chi2Ppf(0.99, i);
        
    nSwitches = 0;
    for i in range(0,N) :
        S = zeros([K, K])
        F = zeros([K, K])
        Best[i] = -1;
        bestGOF = 0
        for ie in range(0,K) :
            emp = emps[ie]
            Zstar = emp.predict(times[i,0])
            e = observations[i] - Zstar[0]
            innovation = emp.update(times[i,0], Zstar, e)
            Y = emp.getState()
            actual[i,ie] = Y[0]
            if (emp.getStatus() != FilterStatus.RUNNING) :
                GOFs[i,ie] = 1.959964**2;
                continue;
            V = emp.getVRF();
            SSRs[i,ie] = e * 1/R * e # (1/(R+V[0,0]))
#             Innovations[i,ie] = (innovation @ inv(R*V) @ transpose(innovation))
            GOFs[i,ie] = w*GOFs[i-1,ie] + (1-w)*(SSRs[i,ie])
            vie = (L-ie+1-1);
            if (V[ie, ie] > 1 or GOFs[i,ie] > gofThresholds[vie]) :
#                 print('BAD', i, ie, SSRs[i,ie], GOFs[i,ie], gofThresholds[vie], V[ie,ie] )
                continue;
            if (Best[i] < 0) :
                Best[i] = ie;
                bestGOF = GOFs[i,ie];
            elif (GOFs[i,ie] < bestGOF) : # better; but significant?
                dG = bestGOF - GOFs[i,ie];
                if (dG > chi2Ppf(pSwitch, 1)) :
                    Best[i] = ie;
                    bestGOF = GOFs[i,ie]; 
        if (Best[i] >= 0 and i > 0) :
            BET[i,:] = BET[i-1,:]
            BET[i,:] = AbstractFilter.conformState(order, emps[Best[i]].getState() );
            if (Best[i] != Best[i-1]) :
                nSwitches += 1  
                 
#             S[ie, ie] = GOFs[i,ie];
#             F[ie, ie] = chi2Cdf(S[ie, ie], 1)
#         print(i, A2S(diag(S)))
#         bestRatio = -1;
#         for j in range(0,K) :
#             if (S[j,j] != 0.0) :
#                 for k in range(j+1,K) :
#                     if (S[k,k] != 0.0 and S[k,k] < S[j,j]) :
#                         dS = S[j,j] - S[k,k];
#                         if (dS < chi2Ppf(0.5, 1)) :
#                             continue
#                         S[j,k] = dS
# #                         threshold = chi2Ppf(0.95, 1)
# #                         threshold = fdistPpf(0.95, 1, 2 );
# #                         x = dS / S[j,j]
# #                         x /= threshold;
#                         F[j,k] = dS
#                         if (dS < bestRatio) :
#                             bestRatio = dS;
#                             Best[i] = k; 
# # residual chi2 mean is not dependent on L; do this only for multi-element residuals                        
# #                         F[j,k] = (S[j,k]/(k-j)) /  (S[j,j]/(L-j-1))
# #                         fThreshold = fdistPpf(0.95, (k-j), (L-j-1) );
# #                         F[j,k] /= fThreshold;
# #                         if (F[j,k] < bestRatio)
# #                             bestRatio = F[j,k]
# #                             Best[i] = k;
# # residual chi2 mean is not dependent on L; do this only for multi-element residuals                        
#         if (i > 0 and Best[i] == 5 ) : # != Best[i-1]) :
#             print(i, times[i,0], Best[i], bestRatio, A2S(diag(S)))
#             print(A2S(S))
#             print(A2S(F))
#             return
        
#             for je in range(ie+1,len(emps)) :
#                 if (emps[je]._VRF()[ie, ie] > 1) :
#                     print('>>', ie, je, emps[je].Z[ie], emps[ie].Z[ie] )
#                     print('fr',ie, je, A2S(emps[je].getState(emps[je].getTime())))
#                     emps[je].Z[ie] = emps[ie].Z[ie];
#                     print('to',ie, je, A2S(emps[je].getState(emps[je].getTime())))
#             if (i < 5 and ie == 0 and SSRs[i,0] < 4) :
#                 for j in range(1,len(emps)) :
#                     emps[j].Z[0] = emps[0].Z[0];
#             if (i < 8 and ie == 1 and i > 1 and SSRs[i,1] < 4) :
#                 emps[2].Z[1] = emps[1].Z[1]
#         print('     ', A2S(truth[i,:]) )
#         print('    0', A2S(emps[0].getState(emps[0].getTime())), A2S(diag(emps[0]._VRF())))
#         print('    1', A2S(emps[1].getState(emps[1].getTime())), A2S(diag(emps[1]._VRF())))
#         print('    2', A2S(emps[2].getState(emps[2].getTime())), A2S(diag(emps[2]._VRF())))
#     print(A2S(concatenate([SSRs, Innovations], axis=1)))
#     print(A2S(GOFs))

    D = BET[1:,:] - truth[1:,:]
#     print(A2S(var(D, axis=0)))
    tr = sum(var(D, axis=0));
    print('%5.3f %5d %6.4f, %10.3f %5d' % (w, L, pSwitch, tr, nSwitches))
#     print(order, mean(Innovations[:,order]), var(Innovations[:,order]))
    if (True or tr > 1e4) :
#         print(truth[0:15,:])
#         print(BET)
#         print(A2S(D))
#         print(A2S(std(D, axis=0)))
#         actual = BET;
        M = 1;
        f0 = plt.figure(figsize=(10, 6))
        ax = plt.subplot(1, 1, 1)
    #     ax.plot(times, GOFs)
        plt.title('order %d' % order)
#         ax.plot(times[M:], truth[M:,0], 'r.-', times[M:], observations[M:], 'b.', \
#                 times[M:], actual[M:,0], 'k-', times[M:], actual[M:,1], 'm-', \
#                 times[M:], actual[M:,2], 'c-', times[M:], actual[M:,3], 'g-');
        ax.plot(times[M:], actual[M:,0]-truth[M:,0], 'k-', times[M:], actual[M:,1]-truth[M:,0], 'm-', \
                times[M:], actual[M:,2]-truth[M:,0], 'c-', times[M:], actual[M:,3]-truth[M:,0], 'g-');
        ax2 = ax.twinx() 
        ax2.plot(times[M:], Best[M:], 'y.-')
        f0.tight_layout()
        plt.show()
    
    '''
  1, 0,   6.303073,   4.884882
  2, 0,   2.218534,   1.010665
  2, 1,   2.340498,   9.687764
  3, 0,   3.410600,   1.087129
  3, 1,   0.380322,   1.467683
  3, 2,   1.984270,  14.350510
  4, 0,   0.049769,   0.012144
  4, 1,   4.184896,  14.774742
  4, 2,   0.204774,   1.682303
  5, 0,  10.743694,   2.118895
  5, 1,   1.448050,   4.667719
  5, 2,   8.481378,  74.626338
  6, 0,   0.952081,   0.157385
  6, 1,   6.310094,  18.629822
  6, 2,   2.849539,  25.937561
  7, 0,   3.867918,   0.549970
  7, 1,   0.112314,   0.305136
  7, 2,   3.247072,  29.928216
  8, 0,   0.917849,   0.114448
  8, 1,   0.384585,   0.966260
  8, 2,   0.104558,   0.962601
  9, 0,   2.988086,   0.331678
  9, 1,   0.000468,   0.001092
  9, 2,   0.637359,   5.808766
 10, 0,   0.026364,   0.002636
 10, 1,   1.512730,   3.296248
 10, 2,   0.151776,   1.361220
    
  1, 0,   6.303073,   4.884882
  2, 0,   2.218534,   1.010665
  2, 1,   1.040221,   4.305673
  3, 0,   3.410600,   1.087129
  3, 1,   0.064989,   0.250797
  3, 2,   0.859556,   6.216423
  4, 0,   0.049769,   0.012144
  4, 1,   1.565771,   5.527943
  4, 2,   0.095246,   0.782480
  5, 0,  10.743694,   2.118895
  5, 1,   0.977576,   3.151167
  5, 2,   4.540983,  39.955405
  6, 0,   0.952081,   0.157385
  6, 1,   2.590235,   7.647368
  6, 2,   1.323269,  12.044881
  7, 0,   3.867918,   0.549970
  7, 1,   0.108960,   0.296025
  7, 2,   0.691245,   6.371192
  8, 0,   0.917849,   0.114448
  8, 1,   0.090598,   0.227626
  8, 2,   0.027684,   0.254872
  9, 0,   2.988086,   0.331678
  9, 1,   0.043339,   0.101179
  9, 2,   0.332512,   3.030448
 10, 0,   0.026364,   0.002636
 10, 1,   0.615658,   1.341523
 10, 2,   0.083545,   0.749281
    '''
#     V = emps[2]._VRF()
# #     print(A2S(V))
#     iV = inv(V)
#     print(A2S(iV))
#     (cV, dV) = covarianceToCorrelation(V)
# #     print(A2S(dV))
# #     print(A2S(cV))
#     icV = inv(cV)
# #     print(A2S(icV))
#     iX = correlationToCovariance(icV, 1/dV)
#     print(A2S(iX))
    
def testMvnrand():
    ''' demonstrate that input correlations are preserved for multichannel filters
    '''
    theta = 0.995;
    tau = 1e-3;
    N = 500000;
    u = array([0, 0, 0])
    P = array([[1,0.5, 0.8],[0.5,1,0.2],[0.8,0.2,1]])
    X = multivariate_normal(u, P, N)
    print(A2S(P))
    order = 2;
    op1 = order+1
    innovations = zeros([N,3*op1])
    residuals = zeros([N,3*op1])
    for i in range(0, X.shape[1]) :
        (times, truth, __, __) = \
            generateTestData(order, N, 0.0, array([1000, -100, 50, -15])[i:i+op1], tau, sigma=0)
        observations = truth[:,0] + X[:,i]
        f = makeFMP(order, theta, tau);
        f.start(0.0, truth[0,:])
#         print(A2S(f.getState()))
#         print(A2S(f.predict(times[1])))
        for j in range(1,N)  :
            Zstar = f.predict(times[j,0])
#             print(i,j,times[j,0], Zstar, observations[j])
            e = observations[j] - Zstar[0]
#             print(e)
            innovations[j,i*op1:(i+1)*op1] = e;
            f.update(times[j,0], Zstar, e)
            residuals[j,i*op1:(i+1)*op1] = f.getState() - truth[j,:]
    
    V = f.getVRF()
    print(A2S(V))
    (cV, dV) = covarianceToCorrelation(V)
    print(A2S(dV))
    print(A2S(cV))
    K = cov(residuals, rowvar=False)
#     print(A2S(K))
    
#     print(A2S(K[0:3,0:3]))
#     print(A2S(K[3:6,3:6]))
#     print(A2S(K[6:9,6:9]))
#     print(residuals.shape)
#     
#     print(A2S(mean(residuals,axis=0)))
#     K = cov(residuals, rowvar=False)
    (cK, dK) = covarianceToCorrelation(K)
#     print(A2S(dK))
    print(A2S(cK))
    
    Q0 = concatenate([cV, P[0,1]*cV, P[0,2]*cV],axis=1)
    Q1 = concatenate([P[1,0]*cV, cV, P[1,2]*cV],axis=1)
    Q2 = concatenate([P[2,0]*cV, P[2,1]*cV, cV],axis=1)
    Q = concatenate([Q0, Q1, Q2], axis=0)
    print(A2S(Q/cK))
    
    print(det(cK), det(Q), det(cK+Q))
    print(N, 'H', hellingerDistance(0*diag(Q), Q, 0*diag(cK), cK) )
    """
500000 H 0.036667127445717866    
    """
        
        
def EmpVrfCorrelation(n : float):
    V = array([[(7 * n ** 3 + 22 * n ** 2 + 55 * n + 60) / (n * (n ** 3 - n ** 2 - n + 1)), \
                6 * (4 * n ** 2 + 13 * n + 19) / (n * (n ** 3 - n ** 2 - n +1)), \
                18 * (n + 3) / (n * (n ** 3 - n ** 2 - n + 1))],\
                [6 * (4 * n ** 2 + 13 * n + 19) / (n * (n ** 3 - n ** 2 - n + 1)), \
                 12 * ((n - 1) ** 2 + 9 * (n + 2) ** 2) / (n * (n - 1) ** 2 * (n + 1) * (n + 2)),\
                 108 / (n * (n - 1) ** 2 * (n + 1))],\
                [18 * (n + 3) / (n * (n ** 3 - n ** 2 - n + 1)), \
                 108 / (n * (n - 1) ** 2 * (n + 1)), \
                 108 / (n * (n - 1) ** 2 * (n + 1) * (n + 2))]]);
    V = array( [[3*(3*n**2 + 9*n + 8)/(n*(n**2 - 1)),18*(2*n + 3)/(n*(n**2 - 1)), 30/(n**3 -n)],\
       [18*(2*n + 3)/(n*(n**2 - 1)), 12*((n - 1)*(n + 3) + 15*(n + 2)**2)/(n*(n - 1)*(n + 1)*(n + 2)*(n + 3)), 180/(n*(n - 1)*(n + 1)*(n + 3))], \
       [30/(n**3 - n), 180/(n*(n - 1)*(n + 1)*(n + 3)), 180/(n*(n - 1)*(n + 1)*(n + 2)*(n + 3))]]);              
#     print(A2S(V))
    (cV, dV) = covarianceToCorrelation(V)
#     print(A2S(dV))
    print(A2S(cV))
    

def fadingChi2():
    N = 10000;
    X = randn(N, 1);
    X2 = zeros([N,1]);
    S = zeros([N,1]);
    for w in [0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99] :
        L = int(2.0 / (1.0-w)) # effective length [Morrison1969, Table 13.4]
        print(w, L)
        V = (-w+1)/(w+1)
        for i in range(0,N) :
            X2[i,0] = X[i,0]**2
            if (i == 0) :
                S[i,0] = X2[i,0]
            else :
                S[i,0] = (1-w)*X2[i,0] + w*S[i-1,0]
                
        print(A2S(mean(X2)), A2S(var(X2)))
        print(A2S(mean(S)), A2S(var(S)), V*var(X2))
    
            
if __name__ == '__main__':
    pass
#     fadingChi2();
    for i in range(0,100) :
        for l in [25] : # [10, 20, 30, 40] :
            for p in [0.750] : #[0.50, 0.60, 0.70, 0.80, 0.90] :
    #             seed(1)
                testEMPSet(l, p)
#     for n in range(3,100,10) :
#         print(n)
#         EmpVrfCorrelation(n)
    
#     testMvnrand()
#     testEMPPair();
#     FMPVRFCorrelations();
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
#     k = -0.5 # /sqrt(3.0)
#     n = 1.0
#     w0 = k/(n+k)
#     wi = 1.0/(2*(n+k))
#     s = sqrt(n+k)
#     
#     A = wi * array([-s, +s])
#     print((A @ A.T))
        