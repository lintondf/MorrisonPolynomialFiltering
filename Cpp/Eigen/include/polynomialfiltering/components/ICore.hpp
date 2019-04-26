/***** /polynomialfiltering/components/ICore/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_COMPONENTS_ICORE_HPP
#define ___POLYNOMIALFILTERING_COMPONENTS_ICORE_HPP

#include <math.h>
#include <vector>
#include <string>
#include <memory>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>



namespace polynomialfiltering {
    namespace components {
        class ICore {
            public:
                ICore();

                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		t	external time
                ///  @param		dtau	internal step
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                virtual RealVector getGamma(const double t, const double dtau) = 0;

                ///// @brief Get the variance reduction matrix
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Square matrix (order+1) of input to output variance ratios
                /// 
                /// 
                virtual RealMatrix getVRF(const int n) = 0;

                ///// @brief Get the variance reduction factor for the 0th derivative
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  0th derivative input to output variance ratio
                /// 
                virtual double getFirstVRF(const int n) = 0;

                ///// @brief Get the variance reduction factor for the 'order'th derivative
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  'order'th derivative input to output variance ratio
                /// 
                virtual double getLastVRF(const int n) = 0;

                ///// @brief Get the variance reduction matrix diagonal vector for the 'order'th derivative
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  'order'th derivative input to output variance ratio
                /// 
                virtual RealVector getDiagonalVRF(const int n) = 0;
        }; // class ICore 

    }; // namespace components
}; // namespace polynomialfiltering


#endif // ___POLYNOMIALFILTERING_COMPONENTS_ICORE_HPP