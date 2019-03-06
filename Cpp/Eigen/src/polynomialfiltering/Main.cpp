/***** /PolynomialFiltering/Main/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */

#include "polynomialfiltering/Main.hpp"

namespace PolynomialFiltering {
    using namespace Eigen;
    
        AbstractFilter::AbstractFilter (const std::string name) {
            this->setStatus(FilterStatus :: IDLE);
            this->name = name;
        }

        RealMatrix AbstractFilter::stateTransitionMatrix (const long N, const double dt) {
            RealMatrix B;
            long ji;
            double fji;
            B = identity(N);
            for (long i = 0; i < N; i++) {
                for (long j = i + 1; j < N; j++) {
                    ji = j - i;
                    fji = ji;
                    for (double x = 2; x < ji; x++) {
                        fji *= x;
                    }
                    B(i, j) = pow(dt, ji) / fji;
                }
            }
            return B;
        }

        std::string AbstractFilter::getName () {
            return this->name;
        }

        void AbstractFilter::setName (const std::string name) {
            this->name = name;
        }

        FilterStatus AbstractFilter::getStatus () {
            return this->status;
        }

        void AbstractFilter::setStatus (const FilterStatus status) {
            this->status = status;
        }

        ManagedFilterBase::ManagedFilterBase () {
        }

        void ManagedFilterBase::addWithVariance (const double t, const RealVector y, const RealMatrix R, const std::string observationId) {
            this->add(t, y, observationId);
        }

}; // namespace PolynomialFiltering

