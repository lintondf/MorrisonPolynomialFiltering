/***** /polynomialfiltering/filters/FixedMemoryPolynomialFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++ from Python Reference Implementation
 */

#include "polynomialfiltering/filters/FixedMemoryPolynomialFilter.hpp"

#pragma float_control(push)
#pragma float_control(precise, off)
namespace polynomialfiltering {
    namespace filters {
        using namespace Eigen;
        
            FixedMemoryFilter::FixedMemoryFilter (const int order, const int memorySize) : AbstractFilter(order) {
                if (order < 0 || order > 5) {
                    throw ValueError("Polynomial orders < 1 or > 5 are not supported");
                }
                this->order = order;
                this->L = memorySize;
                this->n = 0;
                this->n0 = memorySize;
                this->t0 = 0.0;
                this->t = 0.0;
                this->tau = 0.0;
                this->Z = ArrayXd::Zero(this->order + 1);
                this->tRing = ArrayXd::Zero(memorySize);
                this->yRing = ArrayXd::Zero(memorySize);
                this->status = FilterStatus::IDLE;
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
                RealVector dt(L); ///<  array of delta times
                RealMatrix Tn(L, order+1);
                RealMatrix Tnt(order+1, L); ///<  transpose of Tn
                RealMatrix TntTn(order+1, order+1);
                RealMatrix TntYn(order+1, 1);
                dt = this->tRing - t;
                Tn = this->_getTn(dt);
                Tnt = transpose(Tn);
                TntTn = Tnt * Tn;
                TntYn = Tnt * this->yRing;
                this->Z = solve(TntTn, TntYn);
                return copy(this->Z);
            }

            RealVector FixedMemoryFilter::getState () {
                return this->transitionState(this->t);
            }

            void FixedMemoryFilter::add (const double t, const double y, const int observationId) {
                int idx;
                this->t = t;
                idx = this->n % this->L;
                this->tRing(idx) = t;
                this->yRing(idx) = y;
                this->n += 1;
                if (this->n > this->L) {
                    this->status = FilterStatus::RUNNING;
                } else {
                    this->status = FilterStatus::INITIALIZING;
                }
            }

            RealMatrix FixedMemoryFilter::getVRF () {
                RealMatrix V;
                if (this->n < this->L) {
                    V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                } else {
                    V = this->_transitionVrf(this->t);
                }
                return V;
            }

            double FixedMemoryFilter::getFirstVRF () {
                RealMatrix V;
                V = this->getVRF();
                return V(0, 0);
            }

            double FixedMemoryFilter::getLastVRF () {
                RealMatrix V;
                V = this->getVRF();
                return V(this->order, this->order);
            }

            RealMatrix FixedMemoryFilter::_transitionVrf (const double t) {
                RealVector dt;
                RealMatrix Tn;
                RealMatrix V;
                dt = this->tRing - t;
                Tn = this->_getTn(dt);
                V = inv(transpose(Tn) * Tn);
                return V;
            }

            RealMatrix FixedMemoryFilter::_getTn (const RealVector& dt) {
                RealMatrix Tn;
                RealVector C;
                double fact;
                Tn = ArrayXXd::Zero(dt.size(), this->order + 1);
                Tn.col(0) = ones(dt.size(), 1);
                C = copy(dt);
                fact = 1.0;
                for (int i = 1; i < this->order + 1; i++) {
                    fact /= i;
                    Tn.col(i) = C * fact;
                    C = arrayTimes(C, dt);
                }
                return Tn;
            }

    }; // namespace filters
}; // namespace polynomialfiltering

#pragma float_control(pop)