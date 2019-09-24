/***** /polynomialfiltering/Main/AbstractFilterWithCovariance/
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

 

///// @class AbstractFilterWithCovariance
/// @brief Extends AbstractFilter to support state vector covariance methods.
/// 
public abstract class AbstractFilterWithCovariance extends AbstractFilter {
    
    public AbstractFilterWithCovariance() {}  // auto-generated null constructor


    ///// @brief Constructor
    /// 
    /// 
    ///  @param		order	polynomial order of the filter (state contains order+1 elements)
    ///  @param		name	optional identifying string
    /// 
    
    public AbstractFilterWithCovariance(final int order) {
        this(order, "");
    }
    
    public AbstractFilterWithCovariance (final int order, final String name) {
        super(order,name);
    }
    

    ///// @brief Transition the specified covariance by the specified time step
    /// 
    /// 
    ///  @param		dt	time step
    ///  @param		V	N x N covariance matrix
    /// 
    ///  @return  N x N covariance matrix
    /// 
    
    public DMatrixRMaj transitionCovarianceMatrix (final double dt, final DMatrixRMaj V) {
        DMatrixRMaj F = new DMatrixRMaj();
        DMatrixRMaj C = new DMatrixRMaj();
                
        F = AbstractFilter.stateTransitionMatrix((int) V.getNumRows(), dt);
                
        //  C = (F) * V
        C.reshape( F.numRows, V.numCols );
        CommonOps_DDRM.mult( F, V, C );
        return C;
    }
    

    ///// @brief Transition the current filter covariance matrix to the specified time
    /// 
    /// 
    ///  @param		t	target time
    /// 
    ///  @return  N x N covariance matrix
    /// 
    
    public DMatrixRMaj transitionCovariance (final double t) {
        double dt;
        DMatrixRMaj V = new DMatrixRMaj(); ///<  covariance matrix of the filter
                
        V = this.getCovariance();
                
        dt = t - this.getTime();
        
        //  asssignment.dummy = return ( this.transitionCovarianceMatrix(dt, V))
        DMatrixRMaj tm6 = this.transitionCovarianceMatrix(dt, V);
        return tm6;
    }
    

    ///// @brief Get the current filter covariance matrix
    /// 
    ///  @return  Covariance matrix
    /// 
    
    abstract public DMatrixRMaj getCovariance ();

    ///// @brief Get the variance reduction factor for the 0th derivative
    /// 
    /// 
    ///  @param		None
    /// 
    ///  @return  0th derivative input to output variance ratio
    /// 
    
    public double getFirstVariance () {
        DMatrixRMaj V = new DMatrixRMaj();
                
        V = this.getCovariance();
        
        return  V.get(0, 0);
    }
    

    ///// @brief Get the variance reduction factor for the 'order'th derivative
    /// 
    /// 
    ///  @param		None
    /// 
    ///  @return  'order'th derivative input to output variance ratio
    /// 
    
    public double getLastVariance () {
        DMatrixRMaj V = new DMatrixRMaj();
                
        V = this.getCovariance();
        
        return  V.get(V.getNumRows() - 1, V.getNumCols() - 1);
    }
    
} // class Main

