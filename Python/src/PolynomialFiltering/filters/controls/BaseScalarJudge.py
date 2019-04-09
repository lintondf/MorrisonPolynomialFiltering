''' PolynomialFiltering.filters.controls.IJudge
 (C) Copyright 2019 - Blue Lightning Development, LLC.
 D. F. Linton. support@BlueLightningDevelopment.com

 SPDX-License-Identifier: MIT
 See separate LICENSE file for full text
'''

from typing import List;

from PolynomialFiltering.PythonUtilities import virtual, chi2Cdf, chi2Ppf

from numpy import array, zeros, eye, exp, transpose
from numpy import array as vector;

from PolynomialFiltering.Main import AbstractFilterWithCovariance
from PolynomialFiltering.Components.FadingMemoryPolynomialFilter import makeFMP
from PolynomialFiltering.filters.controls.IJudge import IJudge


class BaseScalarJudge(IJudge):
    """
    Judges the goodness of fit of a filter
    """
    
    '''@chi2Starts : array | chi2 initialization values corresponding to 0.999999 Chi2 probability indexed by filter order'''
    '''@f : AbstractFilterWithCovariance | filter to judge'''
    '''@chi2Smoothing : float | Chi2 smoothing factor for goodness-of-fit; 0 no smoothing; 1 ignore residuals completely'''
    '''@chi2 : float | Chi2 statistic for last update'''
    '''@chi2Smoothed : float | Smoothed Chi2 statistic'''
    '''@editChi2 : float | chi2 threshold to edit observation'''
    '''@gofThreshold : float | goodness-of-fit Chi2 cutoff'''
    
    def __init__(self, f : AbstractFilterWithCovariance, editChi2 : float = 3.0, chi2Smoothing : float = 0.9, gofThreshold : float =0.5):
        # computed via chi2.ppf(1-1e-6, df)
        self.chi2Starts = array([23.92812697687947, 27.631021115871036, 30.664849706154268, 33.37684158165888, 35.88818687961042, 38.258336377145845]);

        self.f = f;
        self.editChi2 = editChi2;
        self.chi2Smoothing = chi2Smoothing;
        self.chi2 = self.chi2Starts[self.f.getOrder()];
        self.chi2Smoothed = self.chi2;
        self.gofThreshold = chi2Ppf(gofThreshold, 1);
        
    @classmethod
    def probabilityToChi2(self, p : float, df : int) -> float:
        return chi2Ppf(p, df);

    @classmethod
    def best(self, pSwitch : float, judges : List[IJudge]) -> int:
        '''@ iBest : int'''
        '''@ bestGOF : float '''
        iBest = -1;
        bestGOF = 0;
        '''@iJ : int'''
        '''@dG : float'''
        for iJ in range(0, len(judges)) :
            if (judges[iJ].getFilter().getLastVariance() < 1.0 and judges[iJ].getGOF() > self.gofThreshold) :
                if (iBest < 0) :
                    iBest = iJ;
                    bestGOF = judges[iJ].getGOF();
                elif (judges[iJ].getGOF() < bestGOF) : # better; but significant?
                    dG = bestGOF - judges[iJ].getGOF();
                    if (dG > chi2Ppf(pSwitch, 1)) :
                        iBest = iJ;
                        bestGOF = judges[iJ].getGOF();
        return iBest;
    
    @virtual
    def scalarUpdate(self, e : float, iR : array ) -> bool:
        if (iR[0,0] == 0) :
            return True;
        self.chi2 = (e * iR[0,0] * e);
        self.chi2Smoothed = self.chi2Smoothing * self.chi2Smoothed + (1-self.chi2Smoothing) * self.chi2;
        return self.chi2 < self.editChi2;

    @virtual
    def vectorUpdate(self, e : vector, iR : array ) -> bool:
        if (iR[0,0] == 0) :
            return True;
        self.chi2 = (e[0] * iR[0,0] * e[0]);
        self.chi2Smoothed = self.chi2Smoothing * self.chi2Smoothed + (1-self.chi2Smoothing) * self.chi2;
        return self.chi2 < self.editChi2;

    @virtual
    def getChi2(self) -> float:
        return self.chi2;
    
    @virtual
    def getFilter(self) ->  AbstractFilterWithCovariance:
        return self.f;
    
    @virtual
    def getGOF(self) -> float:
        return self.chi2Smoothed

# 
#     
# if __name__ == "__main__":
#     fmp = makeFMP(5, 0.99, 0.1);
#     threshold = BaseScalarJudge.probabilityToChi2(0.95, fmp.getOrder()+1);
#     print(threshold)
#     judge = BaseScalarJudge(fmp, threshold, 0.0)
#     i = zeros([6])
#     for e in range(0,10) :
#         chi2 = judge.scalarUpdate(e, eye(1));
#         j = judge.getGOF();
#         print(e, chi2, j)
  