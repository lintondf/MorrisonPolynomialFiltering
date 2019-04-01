/***** /PolynomialFiltering/Components/AbstractRecursiveFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_COMPONENTS_ABSTRACTRECURSIVEFILTER_HPP
#define ___POLYNOMIALFILTERING_COMPONENTS_ABSTRACTRECURSIVEFILTER_HPP

#include <math.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/Main.hpp>


namespace PolynomialFiltering {
    namespace Components {

        ///// @class AbstractRecursiveFilter
        /// @brief Base class for both expanding and fading polynomial filter and their combinations.
        /// 
        /// 
        /// @property		n
        ///  number of samples
        /// @property		n0
        ///  threshold number of samples for valid output
        /// @property		dtau
        ///  delta nominal scaled time step
        /// @property		tau
        ///  nominal scaled time step
        /// @property		t
        ///  time of the last input
        /// @property		Z
        ///  NORMALIZED state vector at time of last input
        /// @property		D
        ///  noralization/denormalization scaling vector; D(tau) = [tau^-0, tau^-1,...tau^-order]
        /// 
        class AbstractRecursiveFilter : public AbstractFilter {
            public:

                ///// @brief Estimate of the FMP fading factor theta to match 0th variance of an EMP
                /// 
                /// 
                ///  @param		order	integer polynomial order
                ///  @param		n	float sample number
                /// 
                static double effectiveTheta(const int order, const double n);

                ///// @brief Constructor
                /// 
                /// 
                ///  @param		order	integer polynomial orer
                ///  @param		tau	nominal time step
                /// 
                AbstractRecursiveFilter(const int order, const double tau);

                ///// @brief Start or restart the filter
                /// 
                /// 
                ///  @param		t	external start time
                ///  @param		Z	state vector in external units
                /// 
                ///  @return   @return		None
                /// 
                /// 
                void start(const double t, const RealVector& Z);

                ///// @brief Predict the filter state (Z*) at time t
                /// 
                /// 
                ///  @param		t	target time
                /// 
                ///  @return  predicted state INTERNAL UNITS
                /// 
                /// 
                RealVector predict(const double t);

                ///// @brief Update the filter state from using the prediction error e
                /// 
                /// 
                ///  @param		t	update time
                ///  @param		Zstar	predicted NORMALIZED state at update time
                ///  @param		e	prediction error (observation - predicted state)
                /// 
                ///  @return  innovation vector
                /// 
                ///  @par Examples
                /// Zstar = self.predict(t)
                /// e = observation[0] - Zstar[0]
                /// self.update(t, Zstar, e )
                /// 
                RealVector update(const double t, const RealVector& Zstar, const double e);

                ///// @brief Return the number of processed observations since start
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Count of processed observations
                /// 
                /// 
                int getN();

                ///// @brief Return the nominal time step for the filter
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Nominal time step (tau) in external units
                /// 
                /// 
                double getTau();

                ///// @brief Return the time of the last processed observation or filter start
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Time in external units
                /// 
                /// 
                double getTime();

                ///// @brief Get the current filter state vector
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  State vector in external units
                /// 
                /// 
                RealVector getState();

                ///// @brief Get the variance reduction factor matrix
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Square matrix (order+1) of input to output variance ratios
                /// 
                /// 
                RealMatrix getVRF();
            protected:
                int n;
                int n0;
                double dtau;
                double t0;
                double tau;
                double t;
                RealVector Z;
                RealVector D;
                
                ///// @brief Matches an input state vector to the filter order
                /// 
                /// Longer state vectors are truncated and short ones are zero filled
                /// 
                /// 
                ///  @param		state	arbitrary length input state vector
                /// 
                ///  @return  conformed state vector with order+1 elements
                /// 
                /// 
                RealVector _conformState(const RealVector& state);
                
                ///// @brief Convert an external time to internal (tau) units
                /// 
                /// 
                ///  @param		t	external time (e.g. seconds)
                /// 
                ///  @return  time in internal units (tau steps since t0)
                /// 
                /// 
                double _normalizeTime(const double t);
                
                ///// @brief Converts external delta time to internal (tau) step units
                /// 
                /// 
                ///  @param		dt	external time step (e.g. seconds)
                /// 
                ///  @return  time step in internal units
                /// 
                /// 
                double _normalizeDeltaTime(const double dt);
                
                ///// @brief Normalize a state vector
                /// 
                /// Multiplies the input state vector by the normalization vector D
                /// 
                /// 
                ///  @param		Z	state vector in external units
                /// 
                ///  @return  state vector in internal units
                /// 
                /// 
                RealVector _normalizeState(const RealVector& Z);
                
                ///// @brief Denormalize a state vector
                /// 
                /// Divides the input state vector by the normalization vector D
                /// 
                /// 
                ///  @param		Z	state vector in internal units
                /// 
                ///  @return  state vector in external units
                /// 
                /// 
                RealVector _denormalizeState(const RealVector& Z);
                
                ///// @brief Compute the parameter for the _gamma method
                /// 
                /// 
                ///  @param		t	external time
                ///  @param		dtau	internal step
                /// 
                ///  @return  parameter based on filter subclass
                /// 
                /// 
                virtual double _gammaParameter(const double t, const double dtau) = 0;
                
                ///// @brief Get the innovation scale vector
                /// 
                /// 
                ///  @param		nOrT	n for EMP; t for FMP
                /// 
                ///  @return  vector (order+1) of (observation-predict) multipliers
                /// 
                virtual RealVector _gamma(const double nOrT) = 0;
                
                ///// @brief Get the variance reduction matrix
                /// 
                /// 
                ///  @param		None
                /// 
                ///  @return  Square matrix (order+1) of input to output variance ratios
                /// 
                /// 
                virtual RealMatrix _VRF() = 0;
        }; // class AbstractRecursiveFilter 

    }; // namespace Components
}; // namespace PolynomialFiltering


#endif // ___POLYNOMIALFILTERING_COMPONENTS_ABSTRACTRECURSIVEFILTER_HPP