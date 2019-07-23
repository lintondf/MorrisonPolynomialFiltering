/***** /polynomialfiltering/components/RecursivePolynomialFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++ from Python Reference Implementation
 */

#include "polynomialfiltering/components/RecursivePolynomialFilter.hpp"

#pragma float_control(push)
#pragma float_control(precise, off)
namespace polynomialfiltering {
    namespace components {
        using namespace Eigen;
        
            RecursivePolynomialFilter::RecursivePolynomialFilter (const int order, const double tau, const std::shared_ptr<ICore> core) : AbstractFilter(order) {
                if (order < 0 || order > 5) {
                    throw ValueError("Polynomial orders < 0 or > 5 are not supported");
                }
                this->n = 0;
                this->core = core;
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

            double RecursivePolynomialFilter::effectiveTheta (const int order, const double n) {
                double factor;
                if (n < 1) {
                    return 0.0;
                }
                factor = 1.148 * order + 2.0367;
                return 1.0 - factor / n;
            }

            void RecursivePolynomialFilter::copyState (const std::shared_ptr<RecursivePolynomialFilter> that) {
                this->n = that->n;
                this->t0 = that->t0;
                this->t = that->t;
                this->tau = that->tau;
                this->D = that->D;
                this->Z = that->Z;
            }

            void RecursivePolynomialFilter::start (const double t, const RealVector& Z) {
                this->n = 0;
                this->t0 = t;
                this->t = t;
                this->Z = this->_normalizeState(this->_conformState(Z));
            }

            RealVector RecursivePolynomialFilter::predict (const double t) {
                RealVector Zstar;
                double dt;
                double dtau;
                RealMatrix F;
                dt = t - this->t;
                dtau = this->_normalizeDeltaTime(dt);
                F = RecursivePolynomialFilter::stateTransitionMatrix(this->order + 1, dtau);
                Zstar = F * this->Z;
                return Zstar;
            }

            RealVector RecursivePolynomialFilter::update (const double t, const RealVector& Zstar, const double e) {
                double dt;
                double dtau;
                RealVector gamma;
                RealVector innovation;
                dt = t - this->t;
                dtau = this->_normalizeDeltaTime(dt);
                gamma = this->core->getGamma(this->_normalizeTime(t), dtau);
                innovation = gamma * e;
                this->Z = (Zstar + innovation);
                this->t = t;
                this->n += 1;
                if (this->n < this->order + 2) {
                    this->setStatus(FilterStatus::INITIALIZING);
                } else {
                    this->setStatus(FilterStatus::RUNNING);
                }
                return innovation;
            }

            int RecursivePolynomialFilter::getN () {
                return this->n;
            }

            double RecursivePolynomialFilter::getTau () {
                return this->tau;
            }

            double RecursivePolynomialFilter::getTime () {
                return this->t;
            }

            RealVector RecursivePolynomialFilter::getState () {
                return this->_denormalizeState(this->Z);
            }

            double RecursivePolynomialFilter::getFirstVRF () {
                if (this->n < this->order + 1) {
                    return 0.0;
                }
                return this->core->getFirstVRF(this->n);
            }

            double RecursivePolynomialFilter::getLastVRF () {
                if (this->n < this->order + 1) {
                    return 0.0;
                }
                return this->core->getLastVRF(this->n);
            }

            RealMatrix RecursivePolynomialFilter::getDiagonalVRF () {
                if (this->n < this->order + 1) {
                    return ArrayXXd::Zero(this->order + 1, this->order + 1);
                }
                return this->core->getDiagonalVRF(this->n);
            }

            RealMatrix RecursivePolynomialFilter::getVRF () {
                RealMatrix V;
                if (this->n < this->order + 1) {
                    return ArrayXXd::Zero(this->order + 1, this->order + 1);
                }
                V = this->core->getVRF(this->n);
                return V;
            }

            RealVector RecursivePolynomialFilter::_conformState (const RealVector& state) {
                RealVector Z;
                return RecursivePolynomialFilter::conformState(this->order, state);
            }

            double RecursivePolynomialFilter::_normalizeTime (const double t) {
                return (t - this->t0) / this->tau;
            }

            double RecursivePolynomialFilter::_normalizeDeltaTime (const double dt) {
                return dt / this->tau;
            }

            RealVector RecursivePolynomialFilter::_normalizeState (const RealVector& Z) {
                return arrayTimes(Z, this->D);
            }

            RealVector RecursivePolynomialFilter::_denormalizeState (const RealVector& Z) {
                return arrayDivide(Z, this->D);
            }

    }; // namespace components
}; // namespace polynomialfiltering

#pragma float_control(pop)