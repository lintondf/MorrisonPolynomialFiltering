/***** /PolynomialFiltering/IManagedFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_IMANAGEDFILTER_HPP
#define ___POLYNOMIALFILTERING_IMANAGEDFILTER_HPP

#include <math.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/Main.hpp>


namespace PolynomialFiltering {
    class IObservationErrorModel {
        public:
            IObservationErrorModel();
            virtual RealMatrix getInverseCovariance(const std::shared_ptr<AbstractFilterWithCovariance> f, const double t, const RealVector& y, const int observationId) = 0;
    }; // class IObservationErrorModel 

    class IManagedFilter {
        public:
            IManagedFilter(const std::string name="");
            virtual double getGoodnessOfFit() = 0;
            virtual void add(const double t, const RealVector& y, const int observationId=0) = 0;
            virtual void setObservationInverseR(const RealMatrix& inverseR) = 0;
            virtual void setObservationErrorModel(const std::shared_ptr<IObservationErrorModel> errorModel) = 0;
    }; // class IManagedFilter 

}; // namespace PolynomialFiltering


#endif // ___POLYNOMIALFILTERING_IMANAGEDFILTER_HPP