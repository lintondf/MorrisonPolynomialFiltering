/***** /PolynomialFiltering/Main/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_MAIN_HPP
#define ___POLYNOMIALFILTERING_MAIN_HPP

#include <math.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>



namespace PolynomialFiltering {
    enum FilterStatus {
        IDLE = 0,
        INITIALIZING = 1,
        RUNNING = 2,
        COASTING = 3,
        RESETING = 4,
    }; // class FilterStatus 

    class AbstractFilter {
        public:
            AbstractFilter(const long order, const std::string name="");
            static RealMatrix stateTransitionMatrix(const long N, const double dt);
            std::string getName();
            void setName(const std::string name);
            FilterStatus getStatus();
            void setStatus(const FilterStatus status);
            virtual RealVector transitionState(const double t);
            virtual long getN() = 0;
            virtual double getTime() = 0;
            virtual RealVector getState() = 0;
        protected:
            long order;
            std::string name;
            FilterStatus status;
    }; // class AbstractFilter 

    class AbstractFilterWithCovariance : public AbstractFilter {
        public:
            AbstractFilterWithCovariance(const long order, const std::string name="");
            static RealMatrix transitionCovarianceMatrix(const long order, const double dt, const RealMatrix& V);
            virtual RealMatrix transitionCovariance(const double t, const RealMatrix& R);
            virtual RealMatrix getCovariance() = 0;
    }; // class AbstractFilterWithCovariance 

}; // namespace PolynomialFiltering


#endif // ___POLYNOMIALFILTERING_MAIN_HPP