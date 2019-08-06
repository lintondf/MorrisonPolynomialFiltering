/***** /polynomialfiltering/Main/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++ from Python Reference Implementation
 */

#include "polynomialfiltering/Main.hpp"

#pragma float_control(push)
#pragma float_control(precise, off)
namespace polynomialfiltering {
    using namespace Eigen;
    
        int AbstractFilter::order;
        std::string AbstractFilter::name;
        FilterStatus AbstractFilter::status;
        AbstractFilter::AbstractFilter (const int order, const std::string name) {
            this->setStatus(FilterStatus::IDLE);
            this->order = order;
            this->name = name;
        }

        RealVector AbstractFilter::conformState (const int order, const RealVector& state) {
            RealVector Z;
            int m;
            Z = ArrayXd::Zero(order + 1);
            m = min(order + 1, state.size());
            Z.segment(0, m) = state.segment(0, m);
            return Z;
        }

        RealMatrix AbstractFilter::stateTransitionMatrix (const int N, const double dt) {
            RealMatrix B;
            int ji;
            double fji;
            B = identity(N);
            for (int i = 0; i < N; i++) {
                for (int j = i + 1; j < N; j++) {
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

        int AbstractFilter::getOrder () {
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

        AbstractFilterWithCovariance::AbstractFilterWithCovariance (const int order, const std::string name) : AbstractFilter(order,name) {
        }

        RealMatrix AbstractFilterWithCovariance::transitionCovarianceMatrix (const double dt, const RealMatrix& V) {
            RealMatrix F;
            F = AbstractFilter::stateTransitionMatrix(int(V.rows()), dt);
            return (F) * V;
        }

        RealMatrix AbstractFilterWithCovariance::transitionCovariance (const double t) {
            double dt;
            RealMatrix V; ///<  covariance matrix of the filter
            V = this->getCovariance();
            dt = t - this->getTime();
            return AbstractFilterWithCovariance::transitionCovarianceMatrix(dt, V);
        }

        double AbstractFilterWithCovariance::getFirstVariance () {
            RealMatrix V;
            V = this->getCovariance();
            return V(0, 0);
        }

        double AbstractFilterWithCovariance::getLastVariance () {
            RealMatrix V;
            V = this->getCovariance();
            return V(V.rows() - 1, V.cols() - 1);
        }

}; // namespace polynomialfiltering

#pragma float_control(pop)