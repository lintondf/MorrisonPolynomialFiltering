/***** /PolynomialFiltering/filters/controls/ConstantObservationErrorModel/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_FILTERS_CONTROLS_CONSTANTOBSERVATIONERRORMODEL_HPP
#define ___POLYNOMIALFILTERING_FILTERS_CONTROLS_CONSTANTOBSERVATIONERRORMODEL_HPP

#include <math.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/Main.hpp>
#include <polynomialfiltering/filters/controls/IObservationErrorModel.hpp>


namespace PolynomialFiltering {
    namespace filters {
        namespace controls {

            ///// @class ConstantObservationErrorModel
            /// @brief Constructor
            /// 
            /// 
            ///  @param		R	constant covariance matrix of a vector observation
            ///  @param		inverseR	inverse of the R matrix; used when inverseR is easily computed.
            /// 
            class ConstantObservationErrorModel : public IObservationErrorModel {
                public:

                    ///// @brief Constructor
                    /// 
                    /// 
                    ///  @param		r	constant covariance of a scalar observation
                    /// 
                    ConstantObservationErrorModel(const double r);

                    ///// @brief Constructor
                    /// 
                    /// 
                    ///  @param		R	constant covariance matrix of a vector observation
                    /// 
                    ConstantObservationErrorModel(const RealMatrix& R);

                    ///// @brief Constructor
                    /// 
                    /// 
                    ///  @param		R	constant covariance matrix of a vector observation
                    ///  @param		inverseR	inverse of the R matrix; used when inverseR is easily computed.
                    /// 
                    ConstantObservationErrorModel(const RealMatrix& R, const RealMatrix& inverseR);

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
                    RealMatrix getPrecisionMatrix(const std::shared_ptr<AbstractFilterWithCovariance> f, const double t, const RealVector& y, const int observationId=-1);

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
                    RealMatrix getCovarianceMatrix(const std::shared_ptr<AbstractFilterWithCovariance> f, const double t, const RealVector& y, const int observationId=-1);
                protected:
                    RealMatrix R; ///<  observation covariance matrix
                    RealMatrix iR; ///<  observation precision (inverse covariance) matrix
            }; // class ConstantObservationErrorModel 

        }; // namespace controls
    }; // namespace filters
}; // namespace PolynomialFiltering


#endif // ___POLYNOMIALFILTERING_FILTERS_CONTROLS_CONSTANTOBSERVATIONERRORMODEL_HPP