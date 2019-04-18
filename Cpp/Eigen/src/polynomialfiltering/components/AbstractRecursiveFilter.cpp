/***** /polynomialfiltering/components/AbstractRecursiveFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */

#include "polynomialfiltering/components/AbstractRecursiveFilter.hpp"

#pragma float_control(push)
#pragma float_control(precise, off)
namespace polynomialfiltering {
    namespace components {
        using namespace Eigen;
        
            double AbstractRecursiveFilter::effectiveTheta (const int order, const double n) {
                double factor;
                if (n < 1) {
                    return 0.0;
                }
                factor = 1.148 * order + 2.0367;
                return 1.0 - factor / n;
            }

            AbstractRecursiveFilter::AbstractRecursiveFilter (const int order, const double tau) : AbstractFilter(order) {
                if (order < 0 || order > 5) {
                    throw ValueError("Polynomial orders < 0 or > 5 are not supported");
                }
                this->n = 0;
                this->n0 = order + 2;
                this->dtau = 0;
                this->t0 = 0;
                this->t = 0;
                this->Z = ArrayXd::Zero(this->order + 1);
                this->tau = tau;
                this->D = ArrayXd::Zero(this->order + 1);
                for (int d = 0; d < this->order + 1; d++) {
                    this->D(d) = pow(this->tau, d);
                }
            }

            void AbstractRecursiveFilter::copyState (const std::shared_ptr<AbstractRecursiveFilter> that) {
                this->n = that->n;
                this->t0 = that->t0;
                this->t = that->t;
                this->tau = that->tau;
                this->D = that->D;
                this->Z = that->Z;
            }

            RealVector AbstractRecursiveFilter::_conformState (const RealVector& state) {
                RealVector Z;
                return AbstractRecursiveFilter::conformState(this->order, state);
            }

            double AbstractRecursiveFilter::_normalizeTime (const double t) {
                return (t - this->t0) / this->tau;
            }

            double AbstractRecursiveFilter::_normalizeDeltaTime (const double dt) {
                return dt / this->tau;
            }

            RealVector AbstractRecursiveFilter::_normalizeState (const RealVector& Z) {
                return arrayTimes(Z, this->D);
            }

            RealVector AbstractRecursiveFilter::_denormalizeState (const RealVector& Z) {
                return arrayDivide(Z, this->D);
            }

            void AbstractRecursiveFilter::start (const double t, const RealVector& Z) {
                this->n = 0;
                this->t0 = t;
                this->t = t;
                this->Z = this->_normalizeState(this->_conformState(Z));
            }

            RealVector AbstractRecursiveFilter::predict (const double t) {
                RealVector Zstar;
                double dt;
                double dtau;
                RealMatrix F;
                dt = t - this->t;
                dtau = this->_normalizeDeltaTime(dt);
                F = AbstractRecursiveFilter::stateTransitionMatrix(this->order + 1, dtau);
                Zstar = F * this->Z;
                return Zstar;
            }

            RealVector AbstractRecursiveFilter::update (const double t, const RealVector& Zstar, const double e) {
                double dt;
                double dtau;
                double p;
                RealVector gamma;
                RealVector innovation;
                dt = t - this->t;
                dtau = this->_normalizeDeltaTime(dt);
                p = this->_gammaParameter(t, dtau);
                gamma = this->_gamma(p);
                innovation = gamma * e;
                this->Z = (Zstar + innovation);
                this->t = t;
                this->n += 1;
                if (this->n < this->n0) {
                    this->setStatus(FilterStatus::INITIALIZING);
                } else {
                    this->setStatus(FilterStatus::RUNNING);
                }
                return innovation;
            }

            int AbstractRecursiveFilter::getN () {
                return this->n;
            }

            double AbstractRecursiveFilter::getTau () {
                return this->tau;
            }

            double AbstractRecursiveFilter::getTime () {
                return this->t;
            }

            RealVector AbstractRecursiveFilter::getState () {
                return this->_denormalizeState(this->Z);
            }

            RealMatrix AbstractRecursiveFilter::getVRF () {
                RealMatrix V;
                V = this->_VRF();
                return V;
            }

    }; // namespace components
}; // namespace polynomialfiltering

#pragma float_control(pop)