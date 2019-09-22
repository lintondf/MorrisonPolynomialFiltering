/***** /polynomialfiltering/filters/controls/IJudge/
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

 

///// @class IJudge
/// @brief Judges the goodness of fit of a filter
/// 
/// Called to determine whether to accept or reject the current observation and
/// to estimate th
/// 
public abstract class IJudge {
    
    public IJudge () {
    }
    
    
    abstract public boolean scalarUpdate (final double e, final DMatrixRMaj iR);
    
    abstract public boolean vectorUpdate (final DMatrixRMaj e, final DMatrixRMaj iR);
    
    abstract public double getChi2 ();
    
    abstract public AbstractFilterWithCovariance getFilter ();
    
    abstract public double getGOF ();
} // class controls

