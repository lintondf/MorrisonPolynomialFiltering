/***** /polynomialfiltering/components/Fmp/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED Java from Python Reference Implementation
 */

package polynomialfiltering.components;
 
import java.util.stream.IntStream;
import org.ejml.data.DMatrixRMaj;
import org.ejml.dense.row.CommonOps_DDRM;
import polynomialfiltering.main.FilterStatus;
import polynomialfiltering.main.AbstractFilter;
import polynomialfiltering.main.AbstractFilterWithCovariance;
import static polynomialfiltering.main.Utility.*;
import polynomialfiltering.components.ICore;
import polynomialfiltering.components.fmp.AbstractCoreFmp;
import polynomialfiltering.components.fmp.CoreFmp0;
import polynomialfiltering.components.fmp.CoreFmp1;
import polynomialfiltering.components.fmp.CoreFmp2;
import polynomialfiltering.components.fmp.CoreFmp3;
import polynomialfiltering.components.fmp.CoreFmp4;
import polynomialfiltering.components.fmp.CoreFmp5;
import polynomialfiltering.components.RecursivePolynomialFilter;

 
public class Fmp {
    
    ///// @brief Factory for fading memory polynomial filter cores
    /// 
    /// 
    ///  @param		order	integer polynomial order
    ///  @param		tau	nominal time step
    ///  @param		theta	fading factor [0..1]
    /// 
    ///  @return  fading memory filter core object
    /// 
    
    static public ICore makeFmpCore (final int order, final double tau, final double theta) {
        ICore _makeFmpCore_return_value; ///< auto-generated return variable
        if (order == 0) {
            _makeFmpCore_return_value = new CoreFmp0(tau, theta);
            return _makeFmpCore_return_value;
        } else if (order == 1.0) {
            _makeFmpCore_return_value = new CoreFmp1(tau, theta);
            return _makeFmpCore_return_value;
        } else if (order == 2.0) {
            _makeFmpCore_return_value = new CoreFmp2(tau, theta);
            return _makeFmpCore_return_value;
        } else if (order == 3.0) {
            _makeFmpCore_return_value = new CoreFmp3(tau, theta);
            return _makeFmpCore_return_value;
        } else if (order == 4.0) {
            _makeFmpCore_return_value = new CoreFmp4(tau, theta);
            return _makeFmpCore_return_value;
        } else {
            _makeFmpCore_return_value = new CoreFmp5(tau, theta);
            return _makeFmpCore_return_value;
        }
    }
    
    
    static public RecursivePolynomialFilter makeFmp (final int order, final double tau, final double theta) {
        RecursivePolynomialFilter _makeFmp_return_value = new RecursivePolynomialFilter(); ///< auto-generated return variable
        ICore core;
        core = Fmp.makeFmpCore(order, tau, theta);
        _makeFmp_return_value = new RecursivePolynomialFilter(order, tau, core);
        return _makeFmp_return_value;
    }
} // class Fmp

