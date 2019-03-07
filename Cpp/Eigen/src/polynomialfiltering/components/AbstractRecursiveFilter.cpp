/***** /PolynomialFiltering/Components/AbstractRecursiveFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */

#include "polynomialfiltering/components/AbstractRecursiveFilter.hpp"

namespace PolynomialFiltering {
    namespace Components {
        using namespace Eigen;
        
            double AbstractRecursiveFilter::effectiveTheta (const long order, const double n) {
                double factor;
                if (n < 1) {
                    return 0.0;
                }
                factor = 1.148 * order + 2.0367;
                return 1.0 - factor / n;
            }

            AbstractRecursiveFilter::AbstractRecursiveFilter (const long order, const double tau) : IRecursiveFilter() {
                if (order < 0 || order > 5) {
                    throw ValueError("Polynomial orders < 0 or > 5 are not supported");
                }
                this->n = 0;
                this->n0 = order + 1;
                this->order = order;
                this->dtau = 0;
                this->t0 = 0;
                this->t = 0;
                this->Z = ArrayXd::Zero(this->order + 1);
                this->tau = tau;
                this->D = ArrayXd::Zero(this->order + 1);
                for (long d = 0; d < this->order + 1; d++) {
                    this->D(d) = pow(this->tau, d);
                }
            }

            RealVector AbstractRecursiveFilter::conformState (const RealVector state) {
                RealVector Z;
                long m;
                Z = ArrayXd::Zero(this->order + 1);
                m = std::min(this->order + 1, len(state));
                Z.segment(0, m) = state.segment(0, m);
                return Z;
            }

            void AbstractRecursiveFilter::start (const double t, const RealVector Z) {
                this->n = 0;
                this->t0 = t;
                this->t = t;
                this->Z = this->_normalizeState(this->conformState(Z));
            }

            double AbstractRecursiveFilter::_normalizeTime (const double t) {
                return (t - this->t0) / this->tau;
            }

            double AbstractRecursiveFilter::_normalizeDeltaTime (const double dt) {
                return dt / this->tau;
            }

            RealVector AbstractRecursiveFilter::_denormalizeState (const RealVector Z) {
                return arrayDivide(Z, this->D);
            }

            RealVector AbstractRecursiveFilter::_normalizeState (const RealVector Z) {
                return arrayTimes(Z, this->D);
            }

            std::tuple<RealVector, double, double> AbstractRecursiveFilter::predict (const double t) {
                double dt;
                double dtau;
                RealVector Zstar;
                dt = t - this->t;
                dtau = this->_normalizeDeltaTime(dt);
                Zstar = this->stateTransitionMatrix(this->order + 1, dtau) * this->Z;
                return std::make_tuple(Zstar, dt, dtau);
            }

            void AbstractRecursiveFilter::update (const double t, const double dtau, const RealVector Zstar, const RealVector e) {
                double p;
                RealVector gamma;
                p = this->gammaParameter(t, dtau);
                gamma = this->gamma(p);
                this->Z = (Zstar + arrayTimes(gamma, e));
                this->t = t;
                this->n += 1;
                if (this->n < this->n0) {
                    this->setStatus(FilterStatus::INITIALIZING);
                } else {
                    this->setStatus(FilterStatus::RUNNING);
                }
            }

            long AbstractRecursiveFilter::getN () {
                return this->n;
            }

            double AbstractRecursiveFilter::getTau () {
                return this->tau;
            }

            double AbstractRecursiveFilter::getTime () {
                return this->t;
            }

            RealVector AbstractRecursiveFilter::getState (const double t) {
                RealVector Z;
                if (t == this->t) {
                    return this->_denormalizeState(this->Z);
                } else {
                    Z = this->stateTransitionMatrix(this->order + 1, t - this->t) * this->Z;
                    return this->_denormalizeState(Z);
                }
            }

    }; // namespace Components
}; // namespace PolynomialFiltering

