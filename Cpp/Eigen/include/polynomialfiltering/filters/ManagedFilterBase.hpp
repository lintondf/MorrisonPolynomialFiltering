/***** /polynomialfiltering/filters/ManagedFilterBase/
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
#include <vector>
#include <string>
#include <memory>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/Main.hpp>
#include <polynomialfiltering/components/AbstractRecursiveFilter.hpp>
#include <polynomialfiltering/filters/IManagedFilter.hpp>
#include <polynomialfiltering/filters/controls/IObservationErrorModel.hpp>
#include <polynomialfiltering/filters/controls/IJudge.hpp>
#include <polynomialfiltering/filters/controls/IMonitor.hpp>
#include <polynomialfiltering/filters/controls/ConstantObservationErrorModel.hpp>


namespace polynomialfiltering {
    namespace filters {
        class ManagedFilterBase : public AbstractFilterWithCovariance,IManagedFilter {
            public:
                ManagedFilterBase(const int order, const /*rTS*/std::shared_ptr<components::AbstractRecursiveFilter> worker);
                FilterStatus getStatus();
                int getN();
                double getTime();
                RealVector getState();
                /*rTS*/std::shared_ptr<components::AbstractRecursiveFilter> getWorker();
                void setObservationInverseR(const RealMatrix& inverseR);
                void setObservationErrorModel(const /*rTS*/std::shared_ptr<controls::IObservationErrorModel> errorModel);
                void setJudge(const /*rTS*/std::shared_ptr<controls::IJudge> judge);
                void setMonitor(const /*rTS*/std::shared_ptr<controls::IMonitor> monitor);
                virtual bool add(const double t, const RealVector& y, const int observationId=0) = 0;
                virtual RealMatrix getCovariance() = 0;
                virtual double getGoodnessOfFit() = 0;
            protected:
                double INITIAL_SSR; ///<  start point for smoothed SSR 
                /*rTS*/std::shared_ptr<components::AbstractRecursiveFilter> worker; ///<  that which is managed
                /*rTS*/std::shared_ptr<controls::IObservationErrorModel> errorModel; ///<  observation covariance/precision matrix source
                /*rTS*/std::shared_ptr<controls::IJudge> judge; ///<  residuals-based observation editing and goodness-of-fit evaluator
                /*rTS*/std::shared_ptr<controls::IMonitor> monitor; ///<  filter state monitoring and control
        }; // class ManagedFilterBase 

    }; // namespace filters
}; // namespace polynomialfiltering


#endif // ___POLYNOMIALFILTERING_FILTERS_MANAGEDFILTERBASE_HPP