/***** /polynomialfiltering/filters/controls/errormodel/ConstantObservationErrorModel/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++ from Python Reference Implementation
 */
#ifndef ___POLYNOMIALFILTERING_FILTERS_CONTROLS_ERRORMODEL_CONSTANTOBSERVATIONERRORMODEL_HPP
#define ___POLYNOMIALFILTERING_FILTERS_CONTROLS_ERRORMODEL_CONSTANTOBSERVATIONERRORMODEL_HPP

#include <math.h>
#include <vector>
#include <string>
#include <memory>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>


#include <polynomialfiltering/Main.hpp>
#include <polynomialfiltering/filters/controls/IObservationErrorModel.hpp>


namespace polynomialfiltering {
    namespace filters {
        namespace controls {
            namespace errormodel {

                ///// @class /polynomialfiltering/filters/controls/errormodel/::ConstantObservationErrorModel : <CLASS>; supers(IObservationErrorModel,)
                /// @brief This model is used when the random errors in observations are constant.
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
                        ///  @param		inverseR	inverse of the R matrix; used when inverseR is easily precomputed.
                        /// 
                        ConstantObservationErrorModel(const RealMatrix& R, const RealMatrix& inverseR);
                        RealMatrix getPrecisionMatrix(const std::shared_ptr<AbstractFilterWithCovariance> f, const double t, const RealVector& y, const int observationId=-1);
                        RealMatrix getCovarianceMatrix(const std::shared_ptr<AbstractFilterWithCovariance> f, const double t, const RealVector& y, const int observationId=-1);
                    protected:
                        RealMatrix R; ///<  observation covariance matrix
                        RealMatrix iR; ///<  observation precision (inverse covariance) matrix
                }; // class ConstantObservationErrorModel 

            }; // namespace errormodel
        }; // namespace controls
    }; // namespace filters
}; // namespace polynomialfiltering


#endif // ___POLYNOMIALFILTERING_FILTERS_CONTROLS_ERRORMODEL_CONSTANTOBSERVATIONERRORMODEL_HPP