/***** /polynomialfiltering/components/Fmp/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_COMPONENTS_FMP_HPP
#define ___POLYNOMIALFILTERING_COMPONENTS_FMP_HPP

#include <math.h>
#include <vector>
#include <string>
#include <memory>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/components/ICore.hpp>
#include <polynomialfiltering/components/RecursivePolynomialFilter.hpp>


namespace polynomialfiltering {
    namespace components {
        class AbstractCoreFmp : public ICore {
            public:
                AbstractCoreFmp(const double tau, const double theta);

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
                RealMatrix getVRF(const int n);

                ///// @brief Get the variance reduction factor for the 0th derivative
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  0th derivative input to output variance ratio
                /// 
                double getFirstVRF(const int n);

                ///// @brief Get the variance reduction factor for the 'order'th derivative
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  'order'th derivative input to output variance ratio
                /// 
                double getLastVRF(const int n);

                ///// @brief Get the variance reduction matrix diagonal vector for the 'order'th derivative
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  'order'th derivative input to output variance ratio
                /// 
                RealMatrix getDiagonalVRF(const int n);
            protected:
                double theta;
                RealMatrix VRF;
                virtual RealMatrix _getVRF(const double tau, const double theta) = 0;
        }; // class AbstractCoreFmp 

        class CoreFmp0 : public AbstractCoreFmp {
            public:
                CoreFmp0(const double tau, const double theta);

                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		t	external time
                ///  @param		dtau	internal step
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector getGamma(const double time, const double dtau);
            protected:
                RealMatrix _getVRF(const double u, const double t);
        }; // class CoreFmp0 

        class CoreFmp1 : public AbstractCoreFmp {
            public:
                CoreFmp1(const double tau, const double theta);

                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		t	external time
                ///  @param		dtau	internal step
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector getGamma(const double time, const double dtau);
            protected:
                RealMatrix _getVRF(const double u, const double t);
        }; // class CoreFmp1 

        class CoreFmp2 : public AbstractCoreFmp {
            public:
                CoreFmp2(const double tau, const double theta);

                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		t	external time
                ///  @param		dtau	internal step
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector getGamma(const double time, const double dtau);
            protected:
                RealMatrix _getVRF(const double u, const double t);
        }; // class CoreFmp2 

        class CoreFmp3 : public AbstractCoreFmp {
            public:
                CoreFmp3(const double tau, const double theta);

                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		t	external time
                ///  @param		dtau	internal step
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector getGamma(const double time, const double dtau);
            protected:
                RealMatrix _getVRF(const double u, const double t);
        }; // class CoreFmp3 

        class CoreFmp4 : public AbstractCoreFmp {
            public:
                CoreFmp4(const double tau, const double theta);

                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		t	external time
                ///  @param		dtau	internal step
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector getGamma(const double time, const double dtau);
            protected:
                RealMatrix _getVRF(const double u, const double t);
        }; // class CoreFmp4 

        class CoreFmp5 : public AbstractCoreFmp {
            public:
                CoreFmp5(const double tau, const double theta);

                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		t	external time
                ///  @param		dtau	internal step
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector getGamma(const double time, const double dtau);
            protected:
                RealMatrix _getVRF(const double u, const double t);
        }; // class CoreFmp5 


        ///// @brief Factory for fading memory polynomial filter cores
        /// 
        /// 
        ///  @param		order	integer polynomial order
        ///  @param		tau	nominal time step
        ///  @param		theta	fading factor [0..1]
        /// 
        ///  @return  fading memory filter core object
        /// 
        std::shared_ptr<ICore> makeFmpCore(const int order, const double tau, const double theta);
        std::shared_ptr<RecursivePolynomialFilter> makeFmp(const int order, const double tau, const double theta);
    }; // namespace components
}; // namespace polynomialfiltering


#endif // ___POLYNOMIALFILTERING_COMPONENTS_FMP_HPP