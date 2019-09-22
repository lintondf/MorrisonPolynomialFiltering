/***** /polynomialfiltering/components/PairedPolynomialFilter/
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
import polynomialfiltering.components.RecursivePolynomialFilter;
import polynomialfiltering.components.ICore;
import static polynomialfiltering.components.Fmp.makeFmpCore;
import static polynomialfiltering.components.Emp.nSwitch;

 
public class PairedPolynomialFilter extends RecursivePolynomialFilter {
    protected  ICore empCore; ///<  provider of core expanding functions
    protected  ICore fmpCore; ///<  provider of core fading functions
    protected  int threshold;
    protected  double theta;
    
    public PairedPolynomialFilter() {}  // auto-generated null constructor

    
    public PairedPolynomialFilter (final int order, final double tau, final double theta) {
        super(order, tau, Emp.makeEmpCore(order, tau) );
        this.empCore = this.core;
                
        this.fmpCore = Fmp.makeFmpCore(order, tau, theta);
                
        this.theta = theta;
                
        this.threshold = (int) Emp.nSwitch(this.order, this.theta);
    }
    
    
    public DMatrixRMaj update (final double t, final DMatrixRMaj Zstar, final double e) {
        DMatrixRMaj i = new DMatrixRMaj();
                
        i = RecursivePolynomialFilter.update(t, Zstar, e);
        if (this.n == this.threshold) {
            this.core = this.fmpCore;
        }
        return i;
    }
    
    
    public void start (final double t, final DMatrixRMaj Z) {
                
        RecursivePolynomialFilter.start(t, Z);
        this.core = this.empCore;
    }
    
    
    public boolean isFading () {
        boolean isF;
        isF = this.n == this.threshold;
        return isF;
    }
    
} // class components

