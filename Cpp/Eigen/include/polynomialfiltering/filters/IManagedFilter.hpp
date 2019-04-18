/***** /polynomialfiltering/filters/IManagedFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_FILTERS_IMANAGEDFILTER_HPP
#define ___POLYNOMIALFILTERING_FILTERS_IMANAGEDFILTER_HPP

#include <math.h>
#include <vector>
#include <string>
#include <memory>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/Main.hpp>
#include <polynomialfiltering/filters/controls/IObservationErrorModel.hpp>


namespace polynomialfiltering {
    namespace filters {
        class IManagedFilter {
            public:
                IManagedFilter(const std::string name="");
                virtual double getGoodnessOfFit() = 0;
                virtual bool add(const double t, const RealVector& y, const int observationId=0) = 0;
                virtual void setObservationInverseR(const RealMatrix& inverseR) = 0;
                virtual void setObservationErrorModel(const /*rTS*/std::shared_ptr<controls::IObservationErrorModel> errorModel) = 0;
        }; // class IManagedFilter 

    }; // namespace filters
}; // namespace polynomialfiltering


#endif // ___POLYNOMIALFILTERING_FILTERS_IMANAGEDFILTER_HPP