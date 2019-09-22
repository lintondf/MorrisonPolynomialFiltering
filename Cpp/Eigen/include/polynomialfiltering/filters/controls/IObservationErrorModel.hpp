/***** /polynomialfiltering/filters/controls/IObservationErrorModel/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++ from Python Reference Implementation
 */
#ifndef ___POLYNOMIALFILTERING_FILTERS_CONTROLS_IOBSERVATIONERRORMODEL_HPP
#define ___POLYNOMIALFILTERING_FILTERS_CONTROLS_IOBSERVATIONERRORMODEL_HPP

#include <math.h>
#include <vector>
#include <string>
#include <memory>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>


#include <polynomialfiltering/Main.hpp>


namespace polynomialfiltering {
    namespace filters {
        namespace controls {

            ///// @class /polynomialfiltering/filters/controls/::IObservationErrorModel : <CLASS>; supers(ABC,)
            /// @brief Interface for all observation error models.
            /// 
            /// Observation error models provide filters with (potentially varying)
            /// covariance matrices characterising the random errors in observation
            /// elements.  The inverse of the covariance matrix ('precision' matrix)
            /// is more frequently required during filter processing.  Error models
            /// generally can compute this inverse more efficiently than by naive
            /// inverse of the covariance matrix.
            /// 
            class IObservationErrorModel {
                public:

                    ///// @brief Constructor
                    /// 
                    /// 
                    IObservationErrorModel() {};

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
}; // namespace polynomialfiltering


#endif // ___POLYNOMIALFILTERING_FILTERS_CONTROLS_IOBSERVATIONERRORMODEL_HPP