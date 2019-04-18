/***** /polynomialfiltering/filters/controls/BaseScalarJudge/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_FILTERS_CONTROLS_BASESCALARJUDGE_HPP
#define ___POLYNOMIALFILTERING_FILTERS_CONTROLS_BASESCALARJUDGE_HPP

#include <math.h>
#include <vector>
#include <string>
#include <memory>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/Main.hpp>
#include <polynomialfiltering/components/FadingMemoryPolynomialFilter.hpp>
#include <polynomialfiltering/filters/controls/IJudge.hpp>


namespace polynomialfiltering {
    namespace filters {
        namespace controls {

            ///// @class BaseScalarJudge
            /// @brief Judges the goodness of fit of a filter
            /// 
            class BaseScalarJudge : public IJudge {
                public:
                    BaseScalarJudge(const std::shared_ptr<AbstractFilterWithCovariance> f, const double editChi2=3.0, const double chi2Smoothing=0.9, const double gofThreshold=0.5);
                    static double probabilityToChi2(const double p, const int df);
                    static int best(const double pSwitch, const double gofThreshold, const std::vector<std::shared_ptr<IJudge>> judges);
                    virtual bool scalarUpdate(const double e, const RealMatrix& iR);
                    virtual bool vectorUpdate(const RealVector& e, const RealMatrix& iR);
                    virtual double getChi2();
                    virtual std::shared_ptr<AbstractFilterWithCovariance> getFilter();
                    virtual double getGOF();
                protected:
                    RealMatrix chi2Starts; ///<  chi2 initialization values corresponding to 0.999999 Chi2 probability indexed by filter order
                    std::shared_ptr<AbstractFilterWithCovariance> f; ///<  filter to judge
                    double chi2Smoothing; ///<  Chi2 smoothing factor for goodness-of-fit; 0 no smoothing; 1 ignore residuals completely
                    double chi2; ///<  Chi2 statistic for last update
                    double chi2Smoothed; ///<  Smoothed Chi2 statistic
                    double editChi2; ///<  chi2 threshold to edit observation
                    double gofThreshold; ///<  goodness-of-fit Chi2 cutoff
            }; // class BaseScalarJudge 

        }; // namespace controls
    }; // namespace filters
}; // namespace polynomialfiltering


#endif // ___POLYNOMIALFILTERING_FILTERS_CONTROLS_BASESCALARJUDGE_HPP