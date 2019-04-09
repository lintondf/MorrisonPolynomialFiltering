/***** /PolynomialFiltering/filters/controls/BaseScalarJudge/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */

#include "polynomialfiltering/filters/controls/BaseScalarJudge.hpp"

#pragma float_control(push)
#pragma float_control(precise, off)
namespace PolynomialFiltering {
    namespace filters {
        namespace controls {
            using namespace Eigen;
            
                BaseScalarJudge::BaseScalarJudge (const std::shared_ptr<AbstractFilterWithCovariance> f, const double editChi2, const double chi2Smoothing, const double gofThreshold) {
                    this->chi2Starts = Map<RowVectorXd>( new double[6] {23.92812697687947, 27.631021115871036, 30.664849706154268, 33.37684158165888, 35.88818687961042, 38.258336377145845}, 6);
                    this->(*f) = (*f);
                    this->editChi2 = editChi2;
                    this->chi2Smoothing = chi2Smoothing;
                    this->chi2 = this->chi2Starts(this->(*f)->getOrder());
                    this->chi2Smoothed = this->chi2;
                    this->gofThreshold = chi2Ppf(gofThreshold, 1);
                }

                double BaseScalarJudge::probabilityToChi2 (const double p, const int df) {
                    return chi2Ppf(p, df);
                }

                int BaseScalarJudge::best (const double pSwitch, const std::vector<Judge> judges) {
                    int iBest;
                    double bestGOF;
                    iBest =  - 1;
                    bestGOF = 0;
                    double dG;
                    for (int iJ = 0; iJ < judges.size(); iJ++) {
                        if (this->judges(iJ).getFilter->getLastVariance() < 1.0 && this->judges(iJ).getGOF() > this->gofThreshold) {
                            if (iBest < 0) {
                                iBest = iJ;
                                bestGOF = this->judges(iJ).getGOF();
                            } else if (this->judges(iJ).getGOF() < bestGOF) {
                                dG = bestGOF - this->judges(iJ).getGOF();
                                if (dG > chi2Ppf(pSwitch, 1)) {
                                    iBest = iJ;
                                    bestGOF = this->judges(iJ).getGOF();
                                }
                            }
                        }
                    }
                    return iBest;
                }

                bool BaseScalarJudge::scalarUpdate (const double e, const RealMatrix& iR) {
                    if (iR(0, 0) == 0) {
                        return True;
                    }
                    this->chi2 = (e * iR(0, 0) * e);
                    this->chi2Smoothed = this->chi2Smoothing * this->chi2Smoothed + (1 - this->chi2Smoothing) * this->chi2;
                    return this->chi2 < this->editChi2;
                }

                bool BaseScalarJudge::vectorUpdate (const RealVector& e, const RealMatrix& iR) {
                    if (iR(0, 0) == 0) {
                        return True;
                    }
                    this->chi2 = (arrayTimes(e(0), iR(0, 0)));
                    this->chi2Smoothed = this->chi2Smoothing * this->chi2Smoothed + (1 - this->chi2Smoothing) * this->chi2;
                    return this->chi2 < this->editChi2;
                }

                double BaseScalarJudge::getChi2 () {
                    return this->chi2;
                }

                shared_ptr<AbstractFilterWithCovariance> BaseScalarJudge::getFilter () {
                    return this->f;
                }

                double BaseScalarJudge::getGOF () {
                    return this->chi2Smoothed;
                }

        }; // namespace controls
    }; // namespace filters
}; // namespace PolynomialFiltering

#pragma float_control(pop)