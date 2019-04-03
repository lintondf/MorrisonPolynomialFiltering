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

#pragma float_control(push)
#pragma float_control(precise, off)
namespace PolynomialFiltering {
    namespace Components {
        using namespace Eigen;
        
            FixedMemoryFilter::FixedMemoryFilter (const int order, const int memorySize) : AbstractFilterWithCovariance(order) {
                if (order < 0 || order > 5) {
                    throw ValueError("Polynomial orders < 1 or > 5 are not supported");
                }
                this->L = memorySize;
                this->n = 0;
                this->n0 = memorySize;
                this->t0 = 0.0;
                this->t = 0.0;
                this->tau = 1.0;
                this->Z = ArrayXd::Zero(this->order + 1);
                this->tRing = ArrayXd::Zero(memorySize);
                this->yRing = ArrayXd::Zero(memorySize);
            }

            int FixedMemoryFilter::getN () {
                return this->n;
            }

            double FixedMemoryFilter::getTau () {
                return this->tau;
            }

            double FixedMemoryFilter::getTime () {
                return this->t;
            }

            RealVector FixedMemoryFilter::transitionState (const double t) {
                RealVector dt; ///<  array of delta times
                RealMatrix Tn;
                RealMatrix Tnt; ///<  transpose of Tn
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

            RealVector FixedMemoryFilter::getState () {
                return this->transitionState(this->t);
            }

            void FixedMemoryFilter::add (const double t, const double y, const std::string observationId) {
                this->t = t;
                this->tRing(this->n % this->L) = t;
                this->yRing(this->n % this->L) = y;
                this->n += 1;
            }

            RealMatrix FixedMemoryFilter::getCovariance () {
                return this->transitionCovariance(this->t);
            }

            RealMatrix FixedMemoryFilter::transitionCovariance (const double t) {
                RealVector dt;
                RealMatrix Tn;
                dt = this->tRing - t;
                Tn = this->_getTn(dt);
                return inv(transpose(Tn) * Tn);
            }

            RealMatrix FixedMemoryFilter::_getTn (const RealVector& dt) {
                RealMatrix Tn;
                RealVector C;
                double fact;
                Tn = ArrayXXd::Zero(dt.size(), this->order + 1);
                Tn.col(0) = ones(dt.size());
                C = copy(dt);
                fact = 1.0;
                for (int i = 1; i < this->order + 1; i++) {
                    fact /= i;
                    Tn.col(i) = C * fact;
                    C = arrayTimes(C, dt);
                }
                return Tn;
            }

    }; // namespace Components
}; // namespace PolynomialFiltering

#pragma float_control(pop)