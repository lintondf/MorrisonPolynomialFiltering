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

#pragma float_control(push)
#pragma float_control(precise, off)
namespace PolynomialFiltering {
    using namespace Eigen;
    
        AbstractFilter::AbstractFilter (const long order, const std::string name) {
            this->setStatus(FilterStatus::IDLE);
            this->order = order;
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

        long AbstractFilter::getOrder () {
            return this->order;
        }

        FilterStatus AbstractFilter::getStatus () {
            return this->status;
        }

        void AbstractFilter::setStatus (const FilterStatus status) {
            this->status = status;
        }

        RealVector AbstractFilter::transitionState (const double t) {
            double dt;
            RealMatrix F;
            dt = t - this->getTime();
            F = AbstractFilter::stateTransitionMatrix(this->order + 1, dt);
            return F * this->getState();
        }

        AbstractFilterWithCovariance::AbstractFilterWithCovariance (const long order, const std::string name) : AbstractFilter(order,name) {
        }

        RealMatrix AbstractFilterWithCovariance::transitionCovarianceMatrix (const long order, const double dt, const RealMatrix& V) {
            RealMatrix F;
            F = AbstractFilter::stateTransitionMatrix(order + 1, dt);
            return (F) * V;
        }

        RealMatrix AbstractFilterWithCovariance::transitionCovariance (const double t, const RealMatrix& R) {
            double dt;
            RealMatrix F;
            RealMatrix V;
            V = this->getCovariance();
            dt = t - this->getTime();
            return AbstractFilterWithCovariance::transitionCovarianceMatrix(this->order, dt, V);
        }

}; // namespace PolynomialFiltering

#pragma float_control(pop)