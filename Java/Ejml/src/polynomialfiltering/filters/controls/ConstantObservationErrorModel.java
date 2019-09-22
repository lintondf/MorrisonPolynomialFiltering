/***** /polynomialfiltering/filters/controls/ConstantObservationErrorModel/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED Java from Python Reference Implementation
 */

package polynomialfiltering.filters.controls;
 
import java.util.stream.IntStream;
import org.ejml.data.DMatrixRMaj;
import org.ejml.dense.row.CommonOps_DDRM;
import polynomialfiltering.main.FilterStatus;
import polynomialfiltering.main.AbstractFilter;
import polynomialfiltering.main.AbstractFilterWithCovariance;
import static polynomialfiltering.main.Utility.*;
import polynomialfiltering.filters.controls.IObservationErrorModel;

 

///// @class ConstantObservationErrorModel
/// @brief This model is used when the random errors in observations are constant.
/// 
public class ConstantObservationErrorModel extends IObservationErrorModel {
    protected  DMatrixRMaj R = new DMatrixRMaj(); ///<  observation covariance matrix
    protected  DMatrixRMaj iR = new DMatrixRMaj(); ///<  observation precision (inverse covariance) matrix
    
    public ConstantObservationErrorModel() {}  // auto-generated null constructor


    ///// @brief Constructor
    /// 
    /// 
    ///  @param		r	constant covariance of a scalar observation
    /// 
    
    public ConstantObservationErrorModel (final double r) {
        this.R = (new DMatrixRMaj(new double[] {r}));
        this.iR = (new DMatrixRMaj(new double[] {1.0 / r}));
    }
    

    ///// @brief Constructor
    /// 
    /// 
    ///  @param		R	constant covariance matrix of a vector observation
    /// 
    
    public ConstantObservationErrorModel (final DMatrixRMaj R) {
                
        //  this.R = R
        this.R.reshape( R.numRows, R.numCols );
        this.R.set( R );
                
        //  this.iR = inv(R)
        this.iR.reshape( R.numRows, R.numCols );
        boolean ok = CommonOps_DDRM.invert(R, this.iR);
        //TODO check ok;
    }
    

    ///// @brief Constructor
    /// 
    /// 
    ///  @param		R	constant covariance matrix of a vector observation
    ///  @param		inverseR	inverse of the R matrix; used when inverseR is easily computed.
    /// 
    
    public ConstantObservationErrorModel (final DMatrixRMaj R, final DMatrixRMaj inverseR) {
                
        //  this.R = R
        this.R.reshape( R.numRows, R.numCols );
        this.R.set( R );
                
        //  this.iR = inverseR
        this.iR.reshape( inverseR.numRows, inverseR.numCols );
        this.iR.set( inverseR );
    }
    

    ///// @brief Get the precision matrix (inverse covariance) for an observation
    /// 
    /// 
    ///  @param		f	the filter using this model (models can serve multiple filters)
    ///  @param		t	the time of the observation
    ///  @param		y	the observation vector
    ///  @param		observationId	the element of y being used, -1 for all elements
    /// 
    ///  @return  Inverse of the covariance matrix (1x1 if observationId >= 0)
    /// 
    
    public DMatrixRMaj getPrecisionMatrix(final AbstractFilterWithCovariance f, final double t, final DMatrixRMaj y) {
        return getPrecisionMatrix(f, t, y, -1);
    }
    
    public DMatrixRMaj getPrecisionMatrix (final AbstractFilterWithCovariance f, final double t, final DMatrixRMaj y, final int observationId) {
        DMatrixRMaj P = new DMatrixRMaj();
        if (observationId ==  - 1) {
                        
            CommonOps_DDRM.scale( 1.0, this.iR, P );
        } else {
                        
            //  P = this.iR(observationId : (observationId + 1-1), observationId : (observationId + 1-1))
            P.reshape( 1, 1 );
            CommonOps_DDRM.extract( this.iR, observationId, (observationId + 1), observationId, (observationId + 1), P );
        }
        return P;
    }
    

    ///// @brief Get the covariance matrix for an observation
    /// 
    /// 
    ///  @param		f	the filter using this model (models can serve multiple filters)
    ///  @param		t	the time of the observation
    ///  @param		y	the observation vector
    ///  @param		observationId	the element of y being used, -1 for all elements
    /// 
    ///  @return  Covariance matrix (1x1 if observationId >= 0)
    /// 
    
    public DMatrixRMaj getCovarianceMatrix(final AbstractFilterWithCovariance f, final double t, final DMatrixRMaj y) {
        return getCovarianceMatrix(f, t, y, -1);
    }
    
    public DMatrixRMaj getCovarianceMatrix (final AbstractFilterWithCovariance f, final double t, final DMatrixRMaj y, final int observationId) {
        DMatrixRMaj P = new DMatrixRMaj();
        if (observationId ==  - 1) {
                        
            //  P = this.R
            P.reshape( this.R.numRows, this.R.numCols );
            P.set( this.R );
        } else {
                        
            //  P = this.R(observationId : (observationId + 1-1), observationId : (observationId + 1-1))
            P.reshape( 1, 1 );
            CommonOps_DDRM.extract( this.R, observationId, (observationId + 1), observationId, (observationId + 1), P );
        }
        return P;
    }
    
} // class controls

