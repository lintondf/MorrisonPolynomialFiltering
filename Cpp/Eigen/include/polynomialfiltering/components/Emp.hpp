/***** /polynomialfiltering/components/Emp/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
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

        ///// @class CoreEmp0
        /// @brief     Class for the 0th order expanding memory polynomial filter.
        /// 
        class CoreEmp0 : public ICore {
            public:

                ///// @brief         Constructor
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
                RealVector getDiagonalVRF(const int n);
                RealMatrix getVRF(const int n);
            protected:
                int order;
                double tau;
                double _getFirstVRF(const int n, const double tau);
                double _getLastVRF(const int n, const double tau);
                RealMatrix _getDiagonalVRF(const int n, const double tau);
                RealMatrix _getVRF(const int n, const double tau);
        }; // class CoreEmp0 


        ///// @class CoreEmp1
        /// @brief     Class for the 1st order expanding memory polynomial filter.
        /// 
        class CoreEmp1 : public ICore {
            public:

                ///// @brief         Constructor
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
                RealVector getDiagonalVRF(const int n);
                RealMatrix getVRF(const int n);
            protected:
                int order;
                double tau;
                double _getFirstVRF(const int n, const double tau);
                double _getLastVRF(const int n, const double tau);
                RealMatrix _getDiagonalVRF(const int n, const double tau);
                RealMatrix _getVRF(const int n, const double tau);
        }; // class CoreEmp1 


        ///// @class CoreEmp2
        /// @brief     Class for the 2nd order expanding memory polynomial filter.
        /// 
        class CoreEmp2 : public ICore {
            public:

                ///// @brief         Constructor
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
                RealVector getDiagonalVRF(const int n);
                RealMatrix getVRF(const int n);
            protected:
                int order;
                double tau;
                double _getFirstVRF(const int n, const double tau);
                double _getLastVRF(const int n, const double tau);
                RealMatrix _getDiagonalVRF(const int n, const double tau);
                RealMatrix _getVRF(const int n, const double tau);
        }; // class CoreEmp2 


        ///// @class CoreEmp3
        /// @brief     Class for the 3rd order expanding memory polynomial filter.
        /// 
        class CoreEmp3 : public ICore {
            public:

                ///// @brief         Constructor
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
                RealVector getDiagonalVRF(const int n);
                RealMatrix getVRF(const int n);
            protected:
                int order;
                double tau;
                double _getFirstVRF(const int n, const double tau);
                double _getLastVRF(const int n, const double tau);
                RealMatrix _getDiagonalVRF(const int n, const double tau);
                RealMatrix _getVRF(const int n, const double tau);
        }; // class CoreEmp3 


        ///// @class CoreEmp4
        /// @brief     Class for the 4th order expanding memory polynomial filter.
        /// 
        class CoreEmp4 : public ICore {
            public:

                ///// @brief         Constructor
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
                RealVector getDiagonalVRF(const int n);
                RealMatrix getVRF(const int n);
            protected:
                int order;
                double tau;
                double _getFirstVRF(const int n, const double tau);
                double _getLastVRF(const int n, const double tau);
                RealMatrix _getDiagonalVRF(const int n, const double tau);
                RealMatrix _getVRF(const int n, const double tau);
        }; // class CoreEmp4 


        ///// @class CoreEmp5
        /// @brief     Class for the 5th order expanding memory polynomial filter.
        /// 
        class CoreEmp5 : public ICore {
            public:

                ///// @brief         Constructor
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
                RealVector getDiagonalVRF(const int n);
                RealMatrix getVRF(const int n);
            protected:
                int order;
                double tau;
                double _getFirstVRF(const int n, const double tau);
                double _getLastVRF(const int n, const double tau);
                RealMatrix _getDiagonalVRF(const int n, const double tau);
                RealMatrix _getVRF(const int n, const double tau);
        }; // class CoreEmp5 

        double nSwitch(const int order, const double theta);
        if(order==0):         return0;  elif(order==1):         returnmax(order,exp(-0.7469*log(tau)+0.3752));  elif(order==2):         returnmax(order,exp(-0.8363*log(tau)+1.1127));  elif(order==3):         returnmax(order,exp(-0.8753*log(tau)+1.5427));  elif(order==4):         returnmax(order,exp(-0.897*log(tau)+1.8462));  else:         returnmax(order,exp(-0.9108*log(tau)+2.0805)); nUnitLastVRF(const int order, const double tau);

        ///// @brief     Factory for expanding memory polynomial filters
        /// 
        /// 
        ///  @param		order	integer polynomial orer
        ///  @param		tau	nominal time step
        /// 
        ///  @return          expanding memory filter object
        /// 
        std::shared_ptr<ICore> makeEmpCore(const int order, const double tau);
        std::shared_ptr<RecursivePolynomialFilter> makeEmp(const int order, const double tau);
    }; // namespace components
}; // namespace polynomialfiltering


#endif // ___POLYNOMIALFILTERING_COMPONENTS_EMP_HPP