/***** /polynomialfiltering/filters/RecursivePolynomialFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++ from Python Reference Implementation
 */

#include "polynomialfiltering/filters/RecursivePolynomialFilter.hpp"

#pragma float_control(push)
#pragma float_control(precise, off)
namespace polynomialfiltering {
    namespace filters {
        using namespace Eigen;
        
            RecursivePolynomialFilter::RecursivePolynomialFilter (const int order, const double tau, const std::shared_ptr<components::ICore> core) : AbstractFilter(order) {
                double td; ///<  tau^d 
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
                    td = pow(this->tau, d);
                    this->D(d) = td;
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

            void RecursivePolynomialFilter::add (const double t, const double y, const int observationId) {
                RealVector Zstar;
                double e;
                Zstar = this->predict(t);
                e = y - Zstar(0);
                this->update(t, Zstar, e);
            }

            void RecursivePolynomialFilter::start (const double t, const RealVector& Z) {
                this->n = 0;
                this->t0 = t;
                this->t = t;
                this->Z = this->_normalizeState(this->_conformState(Z));
            }

            RealVector RecursivePolynomialFilter::predict (const double t) {
                RealVector Zstar(order+1);
                double dt;
                double dtau;
                RealMatrix F(order+1, order+1);
                dt = t - this->t;
                dtau = this->_normalizeDeltaTime(dt);
                F = RecursivePolynomialFilter::AbstractFilter::stateTransitionMatrix(this->order + 1, dtau);
                Zstar = F * this->Z;
                return Zstar;
            }

            RealVector RecursivePolynomialFilter::update (const double t, const RealVector& Zstar, const double e) {
                double dt;
                double dtau;
                RealVector gamma(order+1);
                RealVector innovation(order+1);
                dt = t - this->t;
                dtau = this->_normalizeDeltaTime(dt);
                gamma = this->core->getGamma(this->_normalizeTime(t), dtau);
                innovation = gamma * e;
                this->Z = (Zstar + innovation);
                this->t = t;
                this->n += 1;
                if (this->n < this->core->getSamplesToStart()) {
                    this->setStatus(FilterStatus::INITIALIZING);
                } else {
                    this->setStatus(FilterStatus::RUNNING);
                }
                return innovation;
            }

            std::shared_ptr<components::ICore> RecursivePolynomialFilter::getCore () {
                return this->core;
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
                if (this->n < this->core->getSamplesToStart()) {
                    return 0.0;
                }
                return this->core->getFirstVRF(this->n);
            }

            double RecursivePolynomialFilter::getLastVRF () {
                if (this->n < this->core->getSamplesToStart()) {
                    return 0.0;
                }
                return this->core->getLastVRF(this->n);
            }

            RealMatrix RecursivePolynomialFilter::getVRF () {
                RealMatrix V(order+1, order+1);
                if (this->n < this->order + 1) {
                    V = ArrayXXd::Zero(this->order + 1, this->order + 1);
                    return V;
                }
                V = this->core->getVRF(this->n);
                return V;
            }

            RealVector RecursivePolynomialFilter::_conformState (const RealVector& state) {
                RealVector Z;
                return AbstractFilter::conformState(this->order, state);
            }

            double RecursivePolynomialFilter::_normalizeTime (const double t) {
                return (t - this->t0) / this->tau;
            }

            double RecursivePolynomialFilter::_normalizeDeltaTime (const double dt) {
                return dt / this->tau;
            }

            RealVector RecursivePolynomialFilter::_normalizeState (const RealVector& Z) {
                RealVector R(order+1);
                R = arrayTimes(Z, this->D);
                return R;
            }

            RealVector RecursivePolynomialFilter::_denormalizeState (const RealVector& Z) {
                RealVector R(order+1);
                R = arrayDivide(Z, this->D);
                return R;
            }

    }; // namespace filters
}; // namespace polynomialfiltering

#pragma float_control(pop)