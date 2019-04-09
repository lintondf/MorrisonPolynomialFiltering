/***** /PolynomialFiltering/filters/ManagedFilterBase/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_FILTERS_MANAGEDFILTERBASE_HPP
#define ___POLYNOMIALFILTERING_FILTERS_MANAGEDFILTERBASE_HPP

#include <math.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/Main.hpp>
#include <polynomialfiltering/components/AbstractRecursiveFilter.hpp>
#include <polynomialfiltering/filters/IManagedFilter.hpp>
#include <polynomialfiltering/filters/controls/IObservationErrorModel.hpp>
#include <polynomialfiltering/filters/controls/IJudge.hpp>
#include <polynomialfiltering/filters/controls/IMonitor.hpp>
#include <polynomialfiltering/filters/controls/ConstantObservationErrorModel.hpp>


namespace PolynomialFiltering {
    namespace filters {
        class ManagedFilterBase : public AbstractFilterWithCovariance,IManagedFilter {
            public:
                ManagedFilterBase(const std::shared_ptr<AbstractRecursiveFilter> worker);
                FilterStatus getStatus();
                int getN();
                double getTime();
                RealVector getState();
                shared_ptr<AbstractRecursiveFilter> getWorker();
                void setObservationInverseR(const RealMatrix& inverseR);
                void setObservationErrorModel(const std::shared_ptr<IObservationErrorModel> errorModel);
                void setJudge(const std::shared_ptr<IJudge> judge);
                void setMonitor(const std::shared_ptr<IMonitor> monitor);
                virtual bool add(const double t, const RealVector& y, const int observationId=0) = 0;
                virtual RealMatrix getCovariance() = 0;
                virtual double getGoodnessOfFit() = 0;
            protected:
                double INITIAL_SSR; ///<  start point for smoothed SSR 
                shared_ptr<AbstractRecursiveFilter> worker; ///<  that which is managed
                shared_ptr<IObservationErrorModel> errorModel; ///<  observation covariance/precision matrix source
                shared_ptr<IJudge> judge; ///<  residuals-based observation editing and goodness-of-fit evaluator
                shared_ptr<IMonitor> monitor; ///<  filter state monitoring and control
        }; // class ManagedFilterBase 

    }; // namespace filters
}; // namespace PolynomialFiltering


#endif // ___POLYNOMIALFILTERING_FILTERS_MANAGEDFILTERBASE_HPP