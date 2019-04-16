/***** /PolynomialFiltering/Components/FadingMemoryPolynomialFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_COMPONENTS_FADINGMEMORYPOLYNOMIALFILTER_HPP
#define ___POLYNOMIALFILTERING_COMPONENTS_FADINGMEMORYPOLYNOMIALFILTER_HPP

#include <math.h>
#include <vector>
#include <string>
#include <memory>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/components/AbstractRecursiveFilter.hpp>


namespace PolynomialFiltering {
    namespace Components {

        ///// @class FMPBase
        /// @brief         Return the fading factor for the filter
        /// 
        /// 
        ///  @param		            None
        /// 
        ///  @return              fading factor
        /// 
        class FMPBase : public AbstractRecursiveFilter {
            public:

                ///// @brief         Constructor
                /// 
                /// 
                ///  @param		order	integer polynomial orer
                ///  @param		theta	fading factor
                ///  @param		tau	nominal time step
                /// 
                FMPBase(const int order, const double theta, const double tau);

                ///// @brief         Return the fading factor for the filter
                /// 
                /// 
                ///  @param		            None
                /// 
                ///  @return              fading factor
                /// 
                double getTheta();
            protected:
                double theta; ///<  fading factor
                
                ///// @brief Compute the parameter for the _gamma method
                /// 
                /// 
                ///  @param		t	external time
                ///  @param		dtau	internal step
                /// 
                ///  @return  parameter based on filter subclass
                /// 
                /// 
                double _gammaParameter(const double t, const double dtau);
        }; // class FMPBase 


        ///// @class FMP0
        /// @brief         Constructor
        /// 
        /// 
        ///  @param		theta	fading factor
        ///  @param		tau	nominal time step
        /// 
        class FMP0 : public FMPBase {
            public:

                ///// @brief         Constructor
                /// 
                /// 
                ///  @param		theta	fading factor
                ///  @param		tau	nominal time step
                /// 
                FMP0(const double theta, const double tau);
            protected:
                
                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		nOrT	n for EMP; t for FMP
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector _gamma(const double t);
                
                ///// @brief Get the variance reduction matrix
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Square matrix (order+1) of input to output variance ratios
                /// 
                /// 
                RealMatrix _VRF();
        }; // class FMP0 


        ///// @class FMP1
        /// @brief         Constructor
        /// 
        /// 
        ///  @param		theta	fading factor
        ///  @param		tau	nominal time step
        /// 
        class FMP1 : public FMPBase {
            public:

                ///// @brief         Constructor
                /// 
                /// 
                ///  @param		theta	fading factor
                ///  @param		tau	nominal time step
                /// 
                FMP1(const double theta, const double tau);
            protected:
                
                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		nOrT	n for EMP; t for FMP
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector _gamma(const double t);
                
                ///// @brief Get the variance reduction matrix
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Square matrix (order+1) of input to output variance ratios
                /// 
                /// 
                RealMatrix _VRF();
        }; // class FMP1 


        ///// @class FMP2
        /// @brief         Constructor
        /// 
        /// 
        ///  @param		theta	fading factor
        ///  @param		tau	nominal time step
        /// 
        class FMP2 : public FMPBase {
            public:

                ///// @brief         Constructor
                /// 
                /// 
                ///  @param		theta	fading factor
                ///  @param		tau	nominal time step
                /// 
                FMP2(const double theta, const double tau);
            protected:
                
                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		nOrT	n for EMP; t for FMP
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector _gamma(const double t);
                
                ///// @brief Get the variance reduction matrix
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Square matrix (order+1) of input to output variance ratios
                /// 
                /// 
                RealMatrix _VRF();
        }; // class FMP2 


        ///// @class FMP3
        /// @brief         Constructor
        /// 
        /// 
        ///  @param		theta	fading factor
        ///  @param		tau	nominal time step
        /// 
        class FMP3 : public FMPBase {
            public:

                ///// @brief         Constructor
                /// 
                /// 
                ///  @param		theta	fading factor
                ///  @param		tau	nominal time step
                /// 
                FMP3(const double theta, const double tau);
            protected:
                
                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		nOrT	n for EMP; t for FMP
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector _gamma(const double t);
                
                ///// @brief Get the variance reduction matrix
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Square matrix (order+1) of input to output variance ratios
                /// 
                /// 
                RealMatrix _VRF();
        }; // class FMP3 


        ///// @class FMP4
        /// @brief         Constructor
        /// 
        /// 
        ///  @param		theta	fading factor
        ///  @param		tau	nominal time step
        /// 
        class FMP4 : public FMPBase {
            public:

                ///// @brief         Constructor
                /// 
                /// 
                ///  @param		theta	fading factor
                ///  @param		tau	nominal time step
                /// 
                FMP4(const double theta, const double tau);
            protected:
                
                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		nOrT	n for EMP; t for FMP
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector _gamma(const double t);
                
                ///// @brief Get the variance reduction matrix
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Square matrix (order+1) of input to output variance ratios
                /// 
                /// 
                RealMatrix _VRF();
        }; // class FMP4 


        ///// @class FMP5
        /// @brief         Constructor
        /// 
        /// 
        ///  @param		theta	fading factor
        ///  @param		tau	nominal time step
        /// 
        class FMP5 : public FMPBase {
            public:

                ///// @brief         Constructor
                /// 
                /// 
                ///  @param		theta	fading factor
                ///  @param		tau	nominal time step
                /// 
                FMP5(const double theta, const double tau);
            protected:
                
                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		nOrT	n for EMP; t for FMP
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector _gamma(const double t);
                
                ///// @brief Get the variance reduction matrix
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Square matrix (order+1) of input to output variance ratios
                /// 
                /// 
                RealMatrix _VRF();
        }; // class FMP5 


        ///// @brief     Factory for fading memory polynomial filters
        /// 
        /// 
        ///  @param		order	integer polynomial orer
        ///  @param		theta	fading factor
        ///  @param		tau	nominal time step
        /// 
        ///  @return          fading memory filter object
        /// 
        std::shared_ptr<FMPBase> makeFMP(const int order, const double theta, const double tau);

        ///// @brief     Compute the fading factor which give the target value
        /// 
        ///     Determines the theta values which yields a VRF[0,0] element with
        ///     the value vrf at the specified order and nominal time step.
        ///     At some orders and tau values the target may not be achievable
        ///     in these cases the theta value yielding the nearest V[0,0] is
        ///     returned.
        /// 
        /// 
        ///  @param		order	integer polynomial orer
        ///  @param		tau	nominal time step
        ///  @param		vrf	target VRF[0,0] value
        /// 
        ///  @return          fading factor
        /// 
        double thetaFromVrf(const int order, const double tau, const double vrf);
    }; // namespace Components
}; // namespace PolynomialFiltering


#endif // ___POLYNOMIALFILTERING_COMPONENTS_FADINGMEMORYPOLYNOMIALFILTER_HPP