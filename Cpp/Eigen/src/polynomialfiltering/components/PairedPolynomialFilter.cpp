/***** /polynomialfiltering/components/PairedPolynomialFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++ from Python Reference Implementation
 */

#include "polynomialfiltering/components/PairedPolynomialFilter.hpp"

#pragma float_control(push)
#pragma float_control(precise, off)
namespace polynomialfiltering {
    namespace components {
        using namespace Eigen;
        
            PairedPolynomialFilter::PairedPolynomialFilter (const int order, const double tau, const double theta) : RecursivePolynomialFilter(order, tau, Emp::makeEmpCore(order, tau) ) {
                this->empCore = this->core;
                this->fmpCore = Fmp::makeFmpCore(order, tau, theta);
                this->theta = theta;
                this->threshold = int(Emp::nSwitch(this->order, this->theta));
            }

            RealVector PairedPolynomialFilter::update (const double t, const RealVector& Zstar, const double e) {
                RealMatrix i;
                i = RecursivePolynomialFilter::update(t, Zstar, e);
                if (this->n == this->threshold) {
                    this->core = this->fmpCore;
                }
                return i;
            }

            void PairedPolynomialFilter::start (const double t, const RealVector& Z) {
                RecursivePolynomialFilter::start(t, Z);
                this->core = this->empCore;
            }

            bool PairedPolynomialFilter::isFading () {
                bool isF;
                isF = this->n == this->threshold;
                return isF;
            }

    }; // namespace components
}; // namespace polynomialfiltering

#pragma float_control(pop)