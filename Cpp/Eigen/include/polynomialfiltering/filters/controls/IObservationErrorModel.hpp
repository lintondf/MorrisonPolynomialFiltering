/***** /PolynomialFiltering/filters/controls/IObservationErrorModel/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_FILTERS_CONTROLS_IOBSERVATIONERRORMODEL_HPP
#define ___POLYNOMIALFILTERING_FILTERS_CONTROLS_IOBSERVATIONERRORMODEL_HPP

#include <math.h>
#include <vector>
#include <string>
#include <memory>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/Main.hpp>


namespace PolynomialFiltering {
    namespace filters {
        namespace controls {

            ///// @class IObservationErrorModel
            /// @brief Get the covariance matrix for an observation
            /// 
            /// 
            ///  @param		f	the filter using this model (models can serve multiple filters)
            ///  @param		t	the time of the observation
            ///  @param		y	the observation vector
            ///  @param		observationId	the element of y being used, -1 for all elements
            /// 
            ///  @return  Covariance matrix (1x1 if observationId >= 0)
            /// 
            class IObservationErrorModel {
                public:

                    ///// @brief Constructor
                    /// 
                    /// 
                    IObservationErrorModel();

                    ///// @brief Get the precision matrix (inverse covariance) for an observation
                    /// 
                    /// 
                    ///  @param		f	the filter using this model (models can serve multiple filters)
                    ///  @param		t	the time of the observation
                    ///  @param		y	the observation vector
                    ///  @param		observationId	the element of y being used, -1 for all elements
                    /// 
                    ///  @return  Inverse of the covariance matrix (1x1 if observationId >= 0)
                    /// 
                    virtual RealMatrix getPrecisionMatrix(const std::shared_ptr<AbstractFilterWithCovariance> f, const double t, const RealVector& y, const int observationId) = 0;

                    ///// @brief Get the covariance matrix for an observation
                    /// 
                    /// 
                    ///  @param		f	the filter using this model (models can serve multiple filters)
                    ///  @param		t	the time of the observation
                    ///  @param		y	the observation vector
                    ///  @param		observationId	the element of y being used, -1 for all elements
                    /// 
                    ///  @return  Covariance matrix (1x1 if observationId >= 0)
                    /// 
                    virtual RealMatrix getCovarianceMatrix(const std::shared_ptr<AbstractFilterWithCovariance> f, const double t, const RealVector& y, const int observationId) = 0;
            }; // class IObservationErrorModel 

        }; // namespace controls
    }; // namespace filters
}; // namespace PolynomialFiltering


#endif // ___POLYNOMIALFILTERING_FILTERS_CONTROLS_IOBSERVATIONERRORMODEL_HPP