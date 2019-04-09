/***** /PolynomialFiltering/Main/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */
#ifndef ___POLYNOMIALFILTERING_MAIN_HPP
#define ___POLYNOMIALFILTERING_MAIN_HPP

#include <math.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>



namespace PolynomialFiltering {

    ///// @class FilterStatus
    /// @brief The FilterStats enumeration defines the possible states of a filter.
    /// 
    ///  	IDLE	Filter is awaiting the first observation
    ///  	INITIALIZING	Filter has processed one or more observations, but status estimate is not reliable
    ///  	RUNNING	Filter status estimate is reliable
    ///  	COASTING	Filter has not received a recent observation, but the predicted status should be usable
    ///  	RESETING	Filter coast interval has been exceed and it will reinitialize on the next observation
    /// 
    enum FilterStatus {
        IDLE = 0,
        INITIALIZING = 1,
        RUNNING = 2,
        COASTING = 3,
        RESETING = 4,
    }; // class FilterStatus 


    ///// @class AbstractFilter
    /// @brief The base class for all of the filters and components in this package.
    /// 
    class AbstractFilter {
        public:

            ///// @brief Base Constructor
            /// 
            /// 
            ///  @param		order	polynomial order of the filter (state contains order+1 elements)
            ///  @param		name	optional identifying string
            /// 
            AbstractFilter(const int order, const std::string name="");

            ///// @brief Matches an input state vector to the filter order
            /// 
            /// Longer state vectors are truncated and short ones are zero filled
            /// 
            /// 
            ///  @param		order	target state vector order
            ///  @param		state	arbitrary length input state vector
            /// 
            ///  @return  conformed state vector with order+1 elements
            /// 
            /// 
            static RealVector conformState(const int order, const RealVector& state);

            ///// @brief Return a state transition matrix of size N for time step dt
            /// 
            /// Returns a Pade' expanded status transition matrix of order N [RMKdR(7)]
            /// P(d)_i,j = (d^(j-i))/(j-i)! where 0 <= i <= j <= N elsewhere zero
            /// 
            /// 
            ///  @param		N	return matrix is (N,N)
            ///  @param		dt	time step
            /// 
            ///  @return  N by N state transition matrix
            /// 
            static RealMatrix stateTransitionMatrix(const int N, const double dt);

            ///// @brief Return the filter name
            /// 
            ///  @return  Name string, empty if none
            /// 
            /// 
            std::string getName();

            ///// @brief Set the filter name
            /// 
            /// 
            ///  @param		name	string name
            /// 
            void setName(const std::string name);

            ///// @brief Return the filter order
            /// 
            ///  @return  integer filter order
            /// 
            int getOrder();

            ///// @brief Return the filter status
            /// 
            ///  @return  FilterStatus enumeration
            /// 
            FilterStatus getStatus();

            ///// @brief Set the filter status
            /// 
            /// 
            ///  @param		status	enumeration value to set
            /// 
            void setStatus(const FilterStatus status);

            ///// @brief Transition the current state to the target time t
            /// 
            /// 
            ///  @param		t	target time
            /// 
            ///  @return  predicted-state (not normalized)
            /// 
            virtual RealVector transitionState(const double t);

            ///// @brief Return the number of observation the filter has processed
            /// 
            ///  @return  Count of observations used
            /// 
            virtual int getN() = 0;

            ///// @brief Return the current filter time
            /// 
            ///  @return  Filter time
            /// 
            virtual double getTime() = 0;

            ///// @brief Returns the current filter state vector
            /// 
            ///  @return  State vector (order+1 elements)
            /// 
            virtual RealVector getState() = 0;
        protected:
            int order; ///<  polynomial order
            std::string name; ///<  name of this filter
            FilterStatus status; ///<  current status
    }; // class AbstractFilter 


    ///// @class AbstractFilterWithCovariance
    /// @brief Extends AbstractFilter to support state vector covariance methods.
    /// 
    class AbstractFilterWithCovariance : public AbstractFilter {
        public:

            ///// @brief Constructor
            /// 
            /// 
            ///  @param		order	polynomial order of the filter (state contains order+1 elements)
            ///  @param		name	optional identifying string
            /// 
            AbstractFilterWithCovariance(const int order, const std::string name="");

            ///// @brief Transition the specified covariance by the specified time step
            /// 
            /// 
            ///  @param		dt	time step
            ///  @param		V	N x N covariance matrix
            /// 
            ///  @return  N x N covariance matrix
            /// 
            static RealMatrix transitionCovarianceMatrix(const double dt, const RealMatrix& V);

            ///// @brief Transition the current filter covariance matrix to the specified time
            /// 
            /// 
            ///  @param		t	target time
            /// 
            ///  @return  N x N covariance matrix
            /// 
            virtual RealMatrix transitionCovariance(const double t);

            ///// @brief Get the current filter covariance matrix
            /// 
            ///  @return  Covariance matrix
            /// 
            virtual RealMatrix getCovariance() = 0;

            ///// @brief Get the variance reduction factor for the 0th derivative
            /// 
            /// 
            ///  @param		None
            /// 
            ///  @return  0th derivative input to output variance ratio
            /// 
            double getFirstVariance();

            ///// @brief Get the variance reduction factor for the 'order'th derivative
            /// 
            /// 
            ///  @param		None
            /// 
            ///  @return  'order'th derivative input to output variance ratio
            /// 
            double getLastVariance();
    }; // class AbstractFilterWithCovariance 

}; // namespace PolynomialFiltering


#endif // ___POLYNOMIALFILTERING_MAIN_HPP