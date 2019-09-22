/***** /polynomialfiltering/filters/controls/IObservationErrorModel/
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

 

///// @class IObservationErrorModel
/// @brief Interface for all observation error models.
/// 
/// Observation error models provide filters with (potentially varying)
/// covariance matrices characterising the random errors in observation
/// elements.  The inverse of the covariance matrix ('precision' matrix)
/// is more frequently required during filter processing.  Error models
/// generally can compute this inverse more efficiently than by naive
/// inverse of the covariance matrix.
/// 
public abstract class IObservationErrorModel {

    ///// @brief Constructor
    /// 
    /// 
    
    public IObservationErrorModel () {
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
    
    abstract public DMatrixRMaj getPrecisionMatrix (final AbstractFilterWithCovariance f, final double t, final DMatrixRMaj y, final int observationId);

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
    
    abstract public DMatrixRMaj getCovarianceMatrix (final AbstractFilterWithCovariance f, final double t, final DMatrixRMaj y, final int observationId);
} // class controls

