import sys
import os
# 
from polynomialfiltering.components.Fmp import makeFmp, makeFmpCore
from TestUtilities import generateTestPolynomial, generateTestData, createTestGroup, writeTestVariable, A2S
from numpy import diag, allclose, log10, zeros, array
from scipy.optimize.zeros import brentq
from numpy.matlib import randn

# from argparse import ArgumentParser
# from argparse import RawDescriptionHelpFormatter
# 
# from sympy import *
# from sympy.abc import t, u

def vrfAt(order : int, u : float, t: float):
    c = makeFmpCore(order, u, t)
    return c.getVRF(0);

def diagMaxTargeting():
    order = 5;
    for u in (0.001, 0.01, 0.1, 1.0, 8.24, 8.25, 10.0, 1000.0) :
#         for t in (0.000001, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 0.999999) :
        for v in (0.5, 0.1, 0.01, 1e-3) :
            
            def targetDiag(t :float ) -> float:
                c = makeFmpCore(order, u, t);
                return max(diag(c.getVRF(0))) - v;
                
            t0 = brentq( targetDiag, 1e-12, 1-1e-12 );
            c = makeFmpCore(order, u, t0);
    #         v11 = (s**3*(-55580. + s*(295400. + s*(-705460. + s*(986510. + s*(-881918.7999999999 + s*(515277. + s*(-191838.53888888887 + (41542.23888888889 - 3999.827222222222*s)*s))))))))/((-2048. + s*(11264. + s*(-28160. + s*(42240. + s*(-42240. + s*(29568. + s*(-14784. + s*(5280. + s*(-1320. + s*(220. + (-22. + s)*s))))))))))*u**2)
            print('%10.6g %12.6g %12.6g' % (u, v, t0) ); #  A2S(diag(c.getVRF(0)))))


def diagMaxValues():
    order = 5;
    u = 1e-1
    v = 1.0;
    def targetDiag(t :float ) -> float:
        c = makeFmpCore(order, u, t);
        return max(diag(c.getVRF(0))) - v;
        
    t0 = brentq( targetDiag, 1e-12, 1-1e-12 );
    v0 = vrfAt(order,u, t0)
    m0 = max(diag(v0))
    print(order, u, t0, m0, log10(1-t0), log10(m0)); # A2S(diag(v1)))
    dt = 1.0 - t0;
    for it in range(1,100) :
        t = t0 + 0.01*dt*it;
        v1 = vrfAt(order,u, t)
        m1 = max(diag(v1))
        print(order, u, t, m1, log10(1-t), log10(m1), (m1-m0)/dt); # A2S(diag(v1)))
        m0 = m1
    s = 1 - t;
    while (log10(m1) > -8) :
        s = s/2;
        t = 1 - s;
        v1 = vrfAt(order,u, t)
        m1 = max(diag(v1))
        print(order, u, t, m1, log10(1-t), log10(m1), (m1-m0)/dt); # A2S(diag(v1)))
        m0 = m1
#     print(t,m1,A2S(diag(v1)))
        
# #     print(u,t0,max(diag(v0)))
#     s = (1 - t0)/2;
#     t = 1 - s;
#     v1 = vrfAt(order,u, t)
#     print(order, u, t, max(diag(v1))); # A2S(diag(v1)))
#     R0 = v1/v0-1;
#     s = s/2;
#     v0 = v1;
# #     t = 1 - s;
# #     v1 = vrfAt(order,u, t)
# #     R1 = v1/v0-1
# #     dR = R1 - R0
# #     s = s/2;
# #     v0 = v1;
# #     R0 = R1;
#     for it in range(0,32) :
#         t = 1 - s;
#         v1 = vrfAt(order,u, t)
#         R1 = v1/v0-1
#         print(order, u, t, max(diag(v1))); # A2S(diag(v1)))
# #         print(A2S((R1 - R0)/dR-1) )
#         dR = R1 - R0
#         s = s/2;
#         v0 = v1;
#         R0 = R0
#         if (allclose(dR, R1-R0) ) :
#             print(t)
#             print(A2S(R1 - R0) )
#             dR = R1 - R0
#             s = s/2;
#             v0 = v1;
#             R0 = R0
#         else :
#             print( A2S(dR))
#             print(A2S(R1-R0))
#             break
        
def vrfMinValues():
    # For 0th order filters, tau not a consideration
    
    # Find critical tau values for filter orders
    for order in range(1,5+1) :
        def targetTau(u : float):
            c = makeFmpCore(order, u, 1e-12);
#             print( order, u, max(diag(c.getVRF(0))))
            return max(diag(c.getVRF(0))) - (1.0+1e-12);
            
        u0 = brentq( targetTau, 1e-6, 1e6 );
        v0 = vrfAt(order,u0,1e-12)
        print(order,u0,1e-12, v0[0,0])
        print(A2S(v0))
            
    for order in range(1,5+1) :
        u = 1e-3
        while (u <= 1000) :
            v = 1.0;
            def targetMaxDiag(t :float ) -> float:
                c = makeFmpCore(order, u, t);
                return max(diag(c.getVRF(0))) - v;
                 
            t0 = brentq( targetMaxDiag, 1e-12, 1-1e-12 );
            v0 = vrfAt(order,u, t0)
            print(order,u,t0,v0[0,0],1-t0,log10(1-t0))
            u = u * 10;
            
def maxConsistentTheta(tau: float, Y: array) :
    def targetMinRatio(t :float) -> float:
        c = makeFmpCore(Y.shape[0]-1, tau, t);
        d = diag(c.getVRF(0))
        return min( d/Y ) - 1e-14**2;
    
    if (targetMinRatio(1-1e-12)) > 0 :
        return 1-1e-12;
    t0 = brentq( targetMinRatio, 1e-12, 1-1e-12 );
    return t0;
    
def lossOfPrecisionThetas():
    for order in range(1,5+1) :
        for u in (1e-3, 1e-2, 1e-1, 1, 1e1, 1e2, 1e3) :
            for t in (1e-3, 1e-2, 1e-1, 0.5, 0.75, 0.9, 0.99, 0.999) :
                c = makeFmpCore(order, u, t);
                print(order, u, t, A2S(c.getGamma(0.0, 1.0)))
                print('  ', A2S(diag(c.getVRF(0))))
                Y = c.getGamma(0.0, 1.0) * randn(order+1,1)
                print('  ', A2S(Y), maxConsistentTheta(u, Y))
#             v = 1.0 + zeros([order+1])
#             t0 = maxConsistentTheta( u, v );
#             v0 = vrfAt(order,u, t0)
#             print(order,u,t0,v0[0,0],v0[-1,-1])

def main(argv=None): # IGNORE:C0111
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)
    lossOfPrecisionThetas();
#     diagMaxValues();
#     vrfMinValues();

#     print('hello:', argv[1])
#     t, u = symbols('t u')
#     lhs = -1.0/72.0*(613067.0*t**11-1489103.0*t**10+320495.0*t**9+990885.0*t**8+350070.0*t**7-539070.0*t**6-738570.0*t**5+181650.0*t**4+313215.0*t**3+99085.0*t**2-51877.0*t-49847.0)
#     rhs = (u**4*(t**11+11.0*t**10+55.0*t**9+165.0*t**8+330.0*t**7+462.0*t**6+462.0*t**5+330.0*t**4+165.0*t**3+55.0*t**2+11.0*t+1.0))
#     print(horner(lhs))
#     print(horner(rhs))
#     print(horner(argv[1]))

    # (t-1.0)**6*(252.0*t**5+126.0*t**4*(t+1.0)+56.0*t**3*(t+1.0)**2+21.0*t**2*(t+1.0)**3+6.0*t*(t+1.0)**4+(t+1.0)**5)/(u**5*(t+1.0)**11)

if __name__ == '__main__':
    main()
    