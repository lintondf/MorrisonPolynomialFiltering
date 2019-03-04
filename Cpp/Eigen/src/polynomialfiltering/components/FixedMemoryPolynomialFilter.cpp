/***** /PolynomialFiltering/Components/FixedMemoryPolynomialFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */

#include "polynomialfiltering/components/FixedMemoryPolynomialFilter.hpp"

namespace PolynomialFiltering {
    namespace Components {
        using namespace Eigen;
        
            FixedMemoryFilter::FixedMemoryFilter (const long order, const long memorySize) : AbstractFilter() {
                this->order = order;
                this->L = memorySize;
                this->n = 0;
                this->n0 = memorySize;
                this->t0 =  0.0 ;
                this->t =  0.0 ;
                this->tau =  1.0 ;
                this->Z = ArrayXd::Zero(this->order + 1);
                this->tRing = ArrayXd::Zero(memorySize);
                this->yRing = ArrayXd::Zero(memorySize);
            }

            long FixedMemoryFilter::getN () {
                return this->n;
            }

            double FixedMemoryFilter::getTau () {
                return this->tau;
            }

            double FixedMemoryFilter::getTime () {
                return this->t;
            }

            RealMatrix FixedMemoryFilter::getState (const double t) {
                RealVector dt;
                RealMatrix Tn;
                RealMatrix Tnt;
                RealMatrix TntTn;
                RealMatrix TntYn;
                dt = this->tRing - t;
                Tn = this->_getTn(dt);
                Tnt = transpose(Tn);
                TntTn = Tnt * Tn;
                TntYn = Tnt * this->yRing;
                this->Z = solve(TntTn, TntYn);
                return this->Z;
            }

            void FixedMemoryFilter::add (const double t, const double y, const std::string observationId) {
                this->t = t;
                this->tRing(this->n % this->L) = t;
                this->yRing(this->n % this->L) = y;
                this->n += 1;
            }

            RealMatrix FixedMemoryFilter::_getTn (const RealVector dt) {
                RealMatrix Tn;
                RealVector C;
                double fact;
                long i;
                Tn = ArrayXXd::Zero(dt.rows(), this->order + 1);
                Tn.col(0) = ones(dt.rows(), 1);
                C = copy(dt);
                fact =  1.0 ;
                for (long i = 1; i < this->order + 1; i++) {
                    fact /= i;
                    Tn.col(i) = C * fact;
                    C = arrayTimes(C, dt);
                }
                return Tn;
            }

    }; // namespace Components
}; // namespace PolynomialFiltering
