/***** /polynomialfiltering/components/Emp/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++ from Python Reference Implementation
 */
#ifndef ___POLYNOMIALFILTERING_COMPONENTS_EMP_HPP
#define ___POLYNOMIALFILTERING_COMPONENTS_EMP_HPP

#include <math.h>
#include <vector>
#include <string>
#include <memory>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/components/ICore.hpp>
#include <polynomialfiltering/components/RecursivePolynomialFilter.hpp>


namespace polynomialfiltering {
    namespace components {

        ///// @class /polynomialfiltering/components/Emp/::CoreEmp0 : <CLASS>; supers(ICore,)
        /// @brief Class for the 0th order expanding memory polynomial filter.
        /// 
        class CoreEmp0 : public ICore {
            public:

                ///// @brief Constructor
                /// 
                /// 
                ///  @param		tau	nominal time step
                /// 
                CoreEmp0(const double tau);

                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		t	external time
                ///  @param		dtau	internal step
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector getGamma(const double n, const double dtau);
                double getFirstVRF(const int n);
                double getLastVRF(const int n);
                RealMatrix getDiagonalVRF(const int n);
                RealMatrix getVRF(const int n);
            protected:
                int order;
                double tau;
                double _getFirstVRF(const double n, const double tau);
                double _getLastVRF(const double n, const double tau);
                RealMatrix _getDiagonalVRF(const double n, const double tau);
                RealMatrix _getVRF(const double n, const double tau);
        }; // class CoreEmp0 


        ///// @class /polynomialfiltering/components/Emp/::CoreEmp1 : <CLASS>; supers(ICore,)
        /// @brief Class for the 1st order expanding memory polynomial filter.
        /// 
        class CoreEmp1 : public ICore {
            public:

                ///// @brief Constructor
                /// 
                /// 
                ///  @param		tau	nominal time step
                /// 
                CoreEmp1(const double tau);

                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		t	external time
                ///  @param		dtau	internal step
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector getGamma(const double n, const double dtau);
                double getFirstVRF(const int n);
                double getLastVRF(const int n);
                RealMatrix getDiagonalVRF(const int n);
                RealMatrix getVRF(const int n);
            protected:
                int order;
                double tau;
                double _getFirstVRF(const double n, const double tau);
                double _getLastVRF(const double n, const double tau);
                RealMatrix _getDiagonalVRF(const double n, const double tau);
                RealMatrix _getVRF(const double n, const double tau);
        }; // class CoreEmp1 


        ///// @class /polynomialfiltering/components/Emp/::CoreEmp2 : <CLASS>; supers(ICore,)
        /// @brief Class for the 2nd order expanding memory polynomial filter.
        /// 
        class CoreEmp2 : public ICore {
            public:

                ///// @brief Constructor
                /// 
                /// 
                ///  @param		tau	nominal time step
                /// 
                CoreEmp2(const double tau);

                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		t	external time
                ///  @param		dtau	internal step
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector getGamma(const double n, const double dtau);
                double getFirstVRF(const int n);
                double getLastVRF(const int n);
                RealMatrix getDiagonalVRF(const int n);
                RealMatrix getVRF(const int n);
            protected:
                int order;
                double tau;
                double _getFirstVRF(const double n, const double tau);
                double _getLastVRF(const double n, const double tau);
                RealMatrix _getDiagonalVRF(const double n, const double tau);
                RealMatrix _getVRF(const double n, const double tau);
        }; // class CoreEmp2 


        ///// @class /polynomialfiltering/components/Emp/::CoreEmp3 : <CLASS>; supers(ICore,)
        /// @brief Class for the 3rd order expanding memory polynomial filter.
        /// 
        class CoreEmp3 : public ICore {
            public:

                ///// @brief Constructor
                /// 
                /// 
                ///  @param		tau	nominal time step
                /// 
                CoreEmp3(const double tau);

                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		t	external time
                ///  @param		dtau	internal step
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector getGamma(const double n, const double dtau);
                double getFirstVRF(const int n);
                double getLastVRF(const int n);
                RealMatrix getDiagonalVRF(const int n);
                RealMatrix getVRF(const int n);
            protected:
                int order;
                double tau;
                double _getFirstVRF(const double n, const double tau);
                double _getLastVRF(const double n, const double tau);
                RealMatrix _getDiagonalVRF(const double n, const double tau);
                RealMatrix _getVRF(const double n, const double tau);
        }; // class CoreEmp3 


        ///// @class /polynomialfiltering/components/Emp/::CoreEmp4 : <CLASS>; supers(ICore,)
        /// @brief Class for the 4th order expanding memory polynomial filter.
        /// 
        class CoreEmp4 : public ICore {
            public:

                ///// @brief Constructor
                /// 
                /// 
                ///  @param		tau	nominal time step
                /// 
                CoreEmp4(const double tau);

                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		t	external time
                ///  @param		dtau	internal step
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector getGamma(const double n, const double dtau);
                double getFirstVRF(const int n);
                double getLastVRF(const int n);
                RealMatrix getDiagonalVRF(const int n);
                RealMatrix getVRF(const int n);
            protected:
                int order;
                double tau;
                double _getFirstVRF(const double n, const double tau);
                double _getLastVRF(const double n, const double tau);
                RealMatrix _getDiagonalVRF(const double n, const double tau);
                RealMatrix _getVRF(const double n, const double tau);
        }; // class CoreEmp4 


        ///// @class /polynomialfiltering/components/Emp/::CoreEmp5 : <CLASS>; supers(ICore,)
        /// @brief Class for the 5th order expanding memory polynomial filter.
        /// 
        class CoreEmp5 : public ICore {
            public:

                ///// @brief Constructor
                /// 
                /// 
                ///  @param		tau	nominal time step
                /// 
                CoreEmp5(const double tau);

                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		t	external time
                ///  @param		dtau	internal step
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                RealVector getGamma(const double n, const double dtau);
                double getFirstVRF(const int n);
                double getLastVRF(const int n);
                RealMatrix getDiagonalVRF(const int n);
                RealMatrix getVRF(const int n);
            protected:
                int order;
                double tau;
                double _getFirstVRF(const double n, const double tau);
                double _getLastVRF(const double n, const double tau);
                RealMatrix _getDiagonalVRF(const double n, const double tau);
                RealMatrix _getVRF(const double n, const double tau);
        }; // class CoreEmp5 


        ///// @brief Estimate the sample number when the first VRF diagonal elements of an EMP/FMP pair will match
        /// 
        /// Uses approximate relationships to estimate the switchover point for an EMP/FMP pair when the
        /// 0th element of the VRF diagonals will match, e.g. approximately equal noise reduction.  The
        /// approximations are more accurate as theta approaches one.
        /// 
        /// 
        ///  @param		order	polynomial filter order
        ///  @param		theta	FMP fading factor
        /// 
        ///  @return   @return		n	estimated crossover sample number
        /// 
        /// 
        static double nSwitch(const int order, const double theta);

        ///// @brief Estimate the sample number when the final VRF diagonal value is one or less
        /// 
        /// Uses curve fits to estimate the sample number when the final VRF diagonal element
        /// first approaches zero.  For larger tau values, will return the first value value
        /// for this element.
        /// 
        /// 
        ///  @param		order	polynomial filter order
        ///  @param		tau	default time step
        /// 
        ///  @return   @return		n	estimated sample number
        /// 
        static int nUnitLastVRF(const int order, const double tau);
        static std::shared_ptr<RecursivePolynomialFilter> makeEmp(const int order, const double tau);
    }; // namespace components
}; // namespace polynomialfiltering


#endif // ___POLYNOMIALFILTERING_COMPONENTS_EMP_HPP