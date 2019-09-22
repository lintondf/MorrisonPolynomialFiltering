/***** /polynomialfiltering/components/Emp/
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
import polynomialfiltering.main.Utility.ValueError;
import polynomialfiltering.components.emp.CoreEmp0;
import polynomialfiltering.components.emp.CoreEmp1;
import polynomialfiltering.components.emp.CoreEmp2;
import polynomialfiltering.components.emp.CoreEmp3;
import polynomialfiltering.components.emp.CoreEmp4;
import polynomialfiltering.components.emp.CoreEmp5;
import polynomialfiltering.components.RecursivePolynomialFilter;

 
public class Emp {
    
    ///// @brief Estimate the sample number when the first VRF diagonal elements of an EMP/FMP pair will match
    /// 
    /// Uses approximate relationships to estimate the switchover point for an EMP/FMP pair when the
    /// 0th element of the VRF diagonals will match, e.g. approximately equal noise reduction.  The
    /// approximations are more accurate as theta approaches one.
    /// 
    /// 
    ///  @param		order	polynomial filter order
    ///  @param		theta	FMP fading factor
    /// 
    ///  @return   @return		n	estimated crossover sample number
    /// 
    /// 
    
    static public double nSwitch (final int order, final double theta) {
        if (1.0 - theta <= 0.0) {
            return 0.0;
        }
        if (order == 0) {
            return 2.0 / (1.0 - theta);
        } else if (order == 1.0) {
            return 3.2 / (1.0 - theta);
        } else if (order == 2.0) {
            return 4.3636 / (1.0 - theta);
        } else if (order == 3.0) {
            return 5.50546 / (1.0 - theta);
        } else if (order == 4.0) {
            return 6.6321 / (1.0 - theta);
        } else if (order == 5.0) {
            return 7.7478 / (1.0 - theta);
        } else {
            throw new ValueError("Polynomial orders < 0.0 or > 5.0 are not supported");
        }
    }
    
    
    ///// @brief Estimate the sample number when the final VRF diagonal value is one or less
    /// 
    /// Uses curve fits to estimate the sample number when the final VRF diagonal element
    /// first approaches zero.  For larger tau values, will return the first value value
    /// for this element.
    /// 
    /// 
    ///  @param		order	polynomial filter order
    ///  @param		tau	default time step
    /// 
    ///  @return   @return		n	estimated sample number
    /// 
    
    static public int nUnitLastVRF (final int order, final double tau) {
        if (order == 0) {
            return 1;
        } else if (order == 1.0) {
            return 1 + (int) Math.max(order, Math.exp((-0.7469 * Math.log(tau) + 0.3752)));
        } else if (order == 2.0) {
            return 1 + (int) Math.max(order, Math.exp((-0.8363 * Math.log(tau) + 1.1127)));
        } else if (order == 3.0) {
            return 1 + (int) Math.max(order, Math.exp((-0.8753 * Math.log(tau) + 1.5427)));
        } else if (order == 4.0) {
            return 1 + (int) Math.max(order, Math.exp((-0.897 * Math.log(tau) + 1.8462)));
        } else {
            return 1 + (int) Math.max(order, Math.exp((-0.9108 * Math.log(tau) + 2.0805)));
        }
    }
    
    
    ///// @brief Factory for expanding memory polynomial filters
    /// 
    /// 
    ///  @param		order	integer polynomial orer
    ///  @param		tau	nominal time step
    /// 
    ///  @return  expanding memory filter object
    /// 
    
    static public ICore makeEmpCore (final int order, final double tau) {
        ICore _makeEmpCore_return_value; ///< auto-generated return variable
        if (order == 0) {
            _makeEmpCore_return_value = new CoreEmp0(tau);
            return _makeEmpCore_return_value;
        } else if (order == 1.0) {
            _makeEmpCore_return_value = new CoreEmp1(tau);
            return _makeEmpCore_return_value;
        } else if (order == 2.0) {
            _makeEmpCore_return_value = new CoreEmp2(tau);
            return _makeEmpCore_return_value;
        } else if (order == 3.0) {
            _makeEmpCore_return_value = new CoreEmp3(tau);
            return _makeEmpCore_return_value;
        } else if (order == 4.0) {
            _makeEmpCore_return_value = new CoreEmp4(tau);
            return _makeEmpCore_return_value;
        } else {
            _makeEmpCore_return_value = new CoreEmp5(tau);
            return _makeEmpCore_return_value;
        }
    }
    
    
    static public RecursivePolynomialFilter makeEmp (final int order, final double tau) {
        RecursivePolynomialFilter _makeEmp_return_value = new RecursivePolynomialFilter(); ///< auto-generated return variable
        ICore core;
        core = Emp.makeEmpCore(order, tau);
        _makeEmp_return_value = new RecursivePolynomialFilter(order, tau, core);
        return _makeEmp_return_value;
    }
} // class Emp

