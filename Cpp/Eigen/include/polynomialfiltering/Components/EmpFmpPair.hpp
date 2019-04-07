/***** /PolynomialFiltering/Components/EmpFmpPair/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_COMPONENTS_EMPFMPPAIR_HPP
#define ___POLYNOMIALFILTERING_COMPONENTS_EMPFMPPAIR_HPP

#include <math.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/components/AbstractRecursiveFilter.hpp>
#include <polynomialfiltering/components/ExpandingMemoryPolynomialFilter.hpp>
#include <polynomialfiltering/components/FadingMemoryPolynomialFilter.hpp>


namespace PolynomialFiltering {
    namespace Components {

        ///// @class EmpFmpPair
        /// @brief Filter composed of an expanding memory and a fading memory filter of the same order.
        /// 
        /// The EMP filter is used to initialize and after the sample number when the 0th order
        /// variance of the EMP filter matches that variance of the FMP at the configured theta
        /// fading factor, we switch to the FMP filter. See Morrison 1969, Section 13.8
        /// 
        class EmpFmpPair : public AbstractRecursiveFilter {
            public:

                ///// @brief Constructor
                /// 
                /// 
                ///  @param		order	integer polynomial orer
                ///  @param		theta	fading factor
                ///  @param		tau	nominal time step
                /// 
                EmpFmpPair(const int order, const double theta, const double tau);
                void start(const double t, const RealVector& Z);
                RealVector predict(const double t);
                RealVector update(const double t, const RealVector& Zstar, const double e);

                ///// @brief Return the number of observation the filter has processed
                /// 
                ///  @return  Count of observations used
                /// 
                int getN();
                double getTau();

                ///// @brief Return the current filter time
                /// 
                ///  @return  Filter time
                /// 
                double getTime();

                ///// @brief Returns the current filter state vector
                /// 
                ///  @return  State vector (order+1 elements)
                /// 
                RealVector getState();
                RealMatrix getVRF();
            protected:
                shared_ptr<EMPBase> emp;
                shared_ptr<FMPBase> fmp;
                shared_ptr<AbstractRecursiveFilter> current;
                double _gammaParameter(const double t, const double dtau);
                RealVector _gamma(const double n);
                RealMatrix _VRF();
        }; // class EmpFmpPair 

    }; // namespace Components
}; // namespace PolynomialFiltering


#endif // ___POLYNOMIALFILTERING_COMPONENTS_EMPFMPPAIR_HPP