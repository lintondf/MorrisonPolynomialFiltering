/***** /polynomialfiltering/filters/controls/IMonitor/
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

 
public abstract class IMonitor {
    
    public IMonitor () {
    }
    
    
    abstract public void accepted (final AbstractFilterWithCovariance f, final double t, final DMatrixRMaj y, final DMatrixRMaj innovation, final int observationId);
    
    abstract public void rejected (final AbstractFilterWithCovariance f, final double t, final DMatrixRMaj y, final DMatrixRMaj innovation, final int observationId);
} // class controls

