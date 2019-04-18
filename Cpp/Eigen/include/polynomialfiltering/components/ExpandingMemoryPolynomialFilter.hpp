/***** /polynomialfiltering/components/ExpandingMemoryPolynomialFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_COMPONENTS_EXPANDINGMEMORYPOLYNOMIALFILTER_HPP
#define ___POLYNOMIALFILTERING_COMPONENTS_EXPANDINGMEMORYPOLYNOMIALFILTER_HPP

#include <math.h>
#include <vector>
#include <string>
#include <memory>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/components/AbstractRecursiveFilter.hpp>


namespace polynomialfiltering {
    namespace components {

        ///// @class EMPBase
        /// @brief     Base class for expanding memory polynomial filters.
        /// 
        ///     This class implements the 'current-estimate' form of the expanding memory polynomial filter.
        /// 
        class EMPBase : public AbstractRecursiveFilter {
            public:

                ///// @brief         Constructor
                /// 
                /// 
                ///  @param		order	integer polynomial orer
                ///  @param		tau	nominal time step
                /// 
                EMPBase(const int order, const double tau);

                ///// @brief         Compute the observation count to switch from EMP to FMP
                /// 
                ///         The 0th element of the EMP VRF declines as the number of observations
                ///         increases.  For the FMP the VRF is constant.  This function returns the
                ///         observation number at which these elements match
                /// 
                /// 
                ///  @param		theta	fading factor at which to switch
                /// 
                ///  @return              matching observation count
                /// 
                /// 
                virtual double nSwitch(const double theta) = 0;
            protected:
                
                ///// @brief         Compute the parameter for the _gamma method
                /// 
                /// 
                ///  @param		t	external time
                ///  @param		dtau	internal step
                /// 
                ///  @return              parameter based on filter subclass
                /// 
                /// 
                double _gammaParameter(const double t, const double dtau);
        }; // class EMPBase 


        ///// @class EMP0
        /// @brief     Class for the 0th order expanding memory polynomial filter.
        /// 
        class EMP0 : public EMPBase {
            public:

                ///// @brief         Constructor
                /// 
                /// 
                ///  @param		tau	nominal time step
                /// 
                EMP0(const double tau);

                ///// @brief         Compute the observation count to switch from EMP to FMP
                /// 
                ///         The 0th element of the EMP VRF declines as the number of observations
                ///         increases.  For the FMP the VRF is constant.  This function returns the
                ///         observation number at which these elements match
                /// 
                /// 
                ///  @param		theta	fading factor at which to switch
                /// 
                ///  @return              matching observation count
                /// 
                /// 
                double nSwitch(const double theta);
            protected:
                
                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		nOrT	n for EMP; t for FMP
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector _gamma(const double n);
                
                ///// @brief Get the variance reduction matrix
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Square matrix (order+1) of input to output variance ratios
                /// 
                /// 
                RealMatrix _VRF();
        }; // class EMP0 


        ///// @class EMP1
        /// @brief     Class for the 1st order expanding memory polynomial filter.
        /// 
        class EMP1 : public EMPBase {
            public:

                ///// @brief         Constructor
                /// 
                /// 
                ///  @param		tau	nominal time step
                /// 
                EMP1(const double tau);

                ///// @brief         Compute the observation count to switch from EMP to FMP
                /// 
                ///         The 0th element of the EMP VRF declines as the number of observations
                ///         increases.  For the FMP the VRF is constant.  This function returns the
                ///         observation number at which these elements match
                /// 
                /// 
                ///  @param		theta	fading factor at which to switch
                /// 
                ///  @return              matching observation count
                /// 
                /// 
                double nSwitch(const double theta);
            protected:
                
                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		nOrT	n for EMP; t for FMP
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector _gamma(const double n);
                
                ///// @brief Get the variance reduction matrix
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Square matrix (order+1) of input to output variance ratios
                /// 
                /// 
                RealMatrix _VRF();
        }; // class EMP1 


        ///// @class EMP2
        /// @brief     Class for the 2nd order expanding memory polynomial filter.
        /// 
        class EMP2 : public EMPBase {
            public:

                ///// @brief         Constructor
                /// 
                /// 
                ///  @param		tau	nominal time step
                /// 
                EMP2(const double tau);

                ///// @brief         Compute the observation count to switch from EMP to FMP
                /// 
                ///         The 0th element of the EMP VRF declines as the number of observations
                ///         increases.  For the FMP the VRF is constant.  This function returns the
                ///         observation number at which these elements match
                /// 
                /// 
                ///  @param		theta	fading factor at which to switch
                /// 
                ///  @return              matching observation count
                /// 
                /// 
                double nSwitch(const double theta);
            protected:
                
                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		nOrT	n for EMP; t for FMP
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector _gamma(const double n);
                
                ///// @brief Get the variance reduction matrix
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Square matrix (order+1) of input to output variance ratios
                /// 
                /// 
                RealMatrix _VRF();
        }; // class EMP2 


        ///// @class EMP3
        /// @brief     Class for the 3rd order expanding memory polynomial filter.
        /// 
        class EMP3 : public EMPBase {
            public:

                ///// @brief         Constructor
                /// 
                /// 
                ///  @param		tau	nominal time step
                /// 
                EMP3(const double tau);

                ///// @brief         Compute the observation count to switch from EMP to FMP
                /// 
                ///         The 0th element of the EMP VRF declines as the number of observations
                ///         increases.  For the FMP the VRF is constant.  This function returns the
                ///         observation number at which these elements match
                /// 
                /// 
                ///  @param		theta	fading factor at which to switch
                /// 
                ///  @return              matching observation count
                /// 
                /// 
                double nSwitch(const double theta);
            protected:
                
                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		nOrT	n for EMP; t for FMP
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector _gamma(const double n);
                
                ///// @brief Get the variance reduction matrix
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Square matrix (order+1) of input to output variance ratios
                /// 
                /// 
                RealMatrix _VRF();
        }; // class EMP3 


        ///// @class EMP4
        /// @brief     Class for the 4th order expanding memory polynomial filter.
        /// 
        class EMP4 : public EMPBase {
            public:

                ///// @brief         Constructor
                /// 
                /// 
                ///  @param		tau	nominal time step
                /// 
                EMP4(const double tau);

                ///// @brief         Compute the observation count to switch from EMP to FMP
                /// 
                ///         The 0th element of the EMP VRF declines as the number of observations
                ///         increases.  For the FMP the VRF is constant.  This function returns the
                ///         observation number at which these elements match
                /// 
                /// 
                ///  @param		theta	fading factor at which to switch
                /// 
                ///  @return              matching observation count
                /// 
                /// 
                double nSwitch(const double theta);
            protected:
                
                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		nOrT	n for EMP; t for FMP
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector _gamma(const double n);
                
                ///// @brief Get the variance reduction matrix
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Square matrix (order+1) of input to output variance ratios
                /// 
                /// 
                RealMatrix _VRF();
        }; // class EMP4 


        ///// @class EMP5
        /// @brief     Class for the 5th order expanding memory polynomial filter.
        /// 
        class EMP5 : public EMPBase {
            public:

                ///// @brief         Constructor
                /// 
                /// 
                ///  @param		tau	nominal time step
                /// 
                EMP5(const double tau);

                ///// @brief         Compute the observation count to switch from EMP to FMP
                /// 
                ///         The 0th element of the EMP VRF declines as the number of observations
                ///         increases.  For the FMP the VRF is constant.  This function returns the
                ///         observation number at which these elements match
                /// 
                /// 
                ///  @param		theta	fading factor at which to switch
                /// 
                ///  @return              matching observation count
                /// 
                /// 
                double nSwitch(const double theta);
            protected:
                
                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		nOrT	n for EMP; t for FMP
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector _gamma(const double n);
                
                ///// @brief Get the variance reduction matrix
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Square matrix (order+1) of input to output variance ratios
                /// 
                /// 
                RealMatrix _VRF();
        }; // class EMP5 


        ///// @brief     Factory for expanding memory polynomial filters
        /// 
        /// 
        ///  @param		order	integer polynomial orer
        ///  @param		tau	nominal time step
        /// 
        ///  @return          expanding memory filter object
        /// 
        /*rTS*/std::shared_ptr<EMPBase> makeEMP(const int order, const double tau);
    }; // namespace components
}; // namespace polynomialfiltering


#endif // ___POLYNOMIALFILTERING_COMPONENTS_EXPANDINGMEMORYPOLYNOMIALFILTER_HPP