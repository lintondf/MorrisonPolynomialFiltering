/***** /polynomialfiltering/Main/AbstractFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED Java from Python Reference Implementation
 */

package polynomialfiltering.main;
 
import java.util.stream.IntStream;
import org.ejml.data.DMatrixRMaj;
import org.ejml.dense.row.CommonOps_DDRM;
import polynomialfiltering.main.FilterStatus;
import polynomialfiltering.main.AbstractFilter;
import polynomialfiltering.main.AbstractFilterWithCovariance;
import static polynomialfiltering.main.Utility.*;

 

///// @class AbstractFilter
/// @brief The base class for all of the filters and components in this package.
/// 
public abstract class AbstractFilter {
    protected  int order; ///<  polynomial order
    protected  String name; ///<  name of this filter
    protected  FilterStatus status; ///<  current status
    
    public AbstractFilter() {}  // auto-generated null constructor


    ///// @brief Base Constructor
    /// 
    /// 
    ///  @param		order	polynomial order of the filter (state contains order+1 elements)
    ///  @param		name	optional identifying string
    /// 
    
    public AbstractFilter(final int order) {
        this(order, "");
    }
    
    public AbstractFilter (final int order, final String name) {
        this.setStatus(FilterStatus.IDLE);
                
        this.order = order;
        this.name = name;
    }
    

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
    
    static public DMatrixRMaj conformState (final int order, final DMatrixRMaj state) {
        DMatrixRMaj Z = new DMatrixRMaj(order+1, 1);
        int m;
                
        //  Z = zeros(order + 1)
        CommonOps_DDRM.fill( Z, 0.0 );
                
        m = Math.min((order + 1), state.getNumElements());
                
        //  Z(0 : (m-1)) = state(0 : (m-1))
        DMatrixRMaj tm8 = new DMatrixRMaj( 1, m );
        CommonOps_DDRM.extract( state, IntStream.iterate(0, n -> n + 1).limit(1+(m - 1 - 0) / 1).toArray(), m, tm8 );
        CommonOps_DDRM.insert( tm8, Z, IntStream.iterate(0, n -> n + 1).limit(1+(m - 1 - 0) / 1).toArray(), m );
        return Z;
    }
    

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
    
    static public DMatrixRMaj stateTransitionMatrix (final int N, final double dt) {
        DMatrixRMaj B = new DMatrixRMaj(N, N);
        int ji;
        double fji;
                
        //  B = identity(N)
        CommonOps_DDRM.setIdentity( B );
        for (int i = 0; i < N; i++) {
            for (int j = i + 1; j < N; j++) {
                                
                ji = j - i;
                                
                fji = ji;
                for (double x = 2; x < ji; x++) {
                    fji *= x;
                }
                                
                B.unsafe_set(i, j, Math.pow(dt, ji) / fji);
            }
        }
        return B;
    }
    

    ///// @brief Return the filter name
    /// 
    ///  @return  Name string, empty if none
    /// 
    /// 
    
    public String getName () {
        return this.name;
    }
    

    ///// @brief Set the filter name
    /// 
    /// 
    ///  @param		name	string name
    /// 
    
    public void setName (final String name) {
        this.name = name;
    }
    

    ///// @brief Return the filter order
    /// 
    ///  @return  integer filter order
    /// 
    
    public int getOrder () {
        return this.order;
    }
    

    ///// @brief Return the filter status
    /// 
    ///  @return  FilterStatus enumeration
    /// 
    
    public FilterStatus getStatus () {
        FilterStatus _getStatus_return_value; ///< auto-generated return variable
        _getStatus_return_value = this.status;
        return _getStatus_return_value;
    }
    

    ///// @brief Set the filter status
    /// 
    /// 
    ///  @param		status	enumeration value to set
    /// 
    
    public void setStatus (final FilterStatus status) {
        this.status = status;
    }
    

    ///// @brief Transition the current state to the target time t
    /// 
    /// 
    ///  @param		t	target time
    /// 
    ///  @return  predicted-state (not normalized)
    /// 
    
    public DMatrixRMaj transitionState (final double t) {
        double dt;
        DMatrixRMaj F = new DMatrixRMaj();
        DMatrixRMaj Z = new DMatrixRMaj(order+1, 1);
                
        dt = t - this.getTime();
                
        F = AbstractFilter.stateTransitionMatrix(this.order + 1, dt);
                
        //  Z = F * this.getState()
        DMatrixRMaj tm5 = this.getState();
        CommonOps_DDRM.mult( F, tm5, Z );
        return Z;
    }
    

    ///// @brief Return the number of observation the filter has processed
    /// 
    ///  @return  Count of observations used
    /// 
    
    abstract public int getN ();

    ///// @brief Return the current filter time
    /// 
    ///  @return  Filter time
    /// 
    
    abstract public double getTime ();

    ///// @brief Returns the current filter state vector
    /// 
    ///  @return  State vector (order+1 elements)
    /// 
    
    abstract public DMatrixRMaj getState ();

    ///// @brief Get the variance reduction factor for the 0th derivative
    /// 
    /// 
    ///  @param		None
    /// 
    ///  @return  0th derivative input to output variance ratio
    /// 
    
    abstract public double getFirstVRF ();

    ///// @brief Get the variance reduction factor for the 'order'th derivative
    /// 
    /// 
    ///  @param		None
    /// 
    ///  @return  'order'th derivative input to output variance ratio
    /// 
    
    abstract public double getLastVRF ();
    
    abstract public DMatrixRMaj getVRF ();
    
    abstract public void add(final double t, final double y);
    abstract public void add (final double t, final double y, final int observationId);
} // class Main

