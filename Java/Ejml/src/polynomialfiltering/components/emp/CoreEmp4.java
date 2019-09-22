/***** /polynomialfiltering/components/Emp/CoreEmp4/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED Java from Python Reference Implementation
 */

package polynomialfiltering.components.emp;
 
import java.util.stream.IntStream;
import org.ejml.data.DMatrixRMaj;
import org.ejml.dense.row.CommonOps_DDRM;
import polynomialfiltering.main.FilterStatus;
import polynomialfiltering.main.AbstractFilter;
import polynomialfiltering.main.AbstractFilterWithCovariance;
import static polynomialfiltering.main.Utility.*;
import polynomialfiltering.components.ICore;

 

///// @class CoreEmp4
/// @brief Class for the 4th order expanding memory polynomial filter.
/// 
public class CoreEmp4 extends ICore {
    protected  int order;
    protected  double tau;
    
    public CoreEmp4() {}  // auto-generated null constructor


    ///// @brief Constructor
    /// 
    /// 
    ///  @param		tau	nominal time step
    /// 
    
    public CoreEmp4 (final double tau) {
                
        this.order = 4;
                
        this.tau = tau;
    }
    
    
    public int getSamplesToStart () {
        return this.order + 2;
    }
    

    ///// @brief Get the innovation scale vector
    /// 
    /// 
    ///  @param		t	external time
    ///  @param		dtau	internal step
    /// 
    ///  @return  vector (order+1) of (observation-predict) multipliers
    /// 
    
    public DMatrixRMaj getGamma (final double n, final double dtau) {
        double n2;
        double n3;
        double n4;
        double denom;
        DMatrixRMaj g = new DMatrixRMaj(5, 1);
                
        n2 = n * n;
                
        n3 = n2 * n;
                
        n4 = n2 * n2;
                
        denom = 1.0 / ((n + 5) * (n + 4) * (n + 3) * (n + 2) * (n + 1));
        g = (new DMatrixRMaj(new double[] {5.0 * (5.0 * n4 + 10.0 * n3 + 55.0 * n2 + 50.0 * n + 24.0), 25.0 * (12.0 * n3 + 18.0 * n2 + 46.0 * n + 20.0), (2.0 * 1.0) * 1050.0 * (n2 + n + 1.0), (3.0 * 2.0 * 1.0) * 700.0 * (2.0 * n + 1.0), (4.0 * 3.0 * 2.0 * 1.0) * 630.0}));
                
        //  g = denom * g
        CommonOps_DDRM.scale( denom, g, g );
        return g;
    }
    
    
    public double getFirstVRF (final int n) {
        return this._getFirstVRF(n, this.tau);
    }
    
    
    public double getLastVRF (final int n) {
        return this._getLastVRF(n, this.tau);
    }
    
    
    public DMatrixRMaj getDiagonalVRF (final int n) {
        
        return  this._getDiagonalVRF(n, this.tau);
    }
    
    
    public DMatrixRMaj getVRF (final int n) {
        
        return  this._getVRF(n, this.tau);
    }
    
    
    protected double _getFirstVRF (final double n, final double tau) {
        return (5.0 * (5.0 * Math.pow(n, 4) + 30.0 * Math.pow(n, 3) + 115.0 * Math.pow(n, 2) + 210.0 * n + 144.0)) / (n * ((Math.pow(n, 4) - 5.0 * Math.pow(n, 3) + 5.0 * Math.pow(n, 2) + 5.0 * n) - 6.0));
    }
    
    
    protected double _getLastVRF (final double n, final double tau) {
        return 25401600.0 / (n * Math.pow(tau, 8) * (n - 3.0) * (n - 2.0) * (n - 1.0) * (n + 1.0) * (n + 2.0) * (n + 3.0) * (n + 4.0) * (n + 5.0));
    }
    
    
    protected DMatrixRMaj _getDiagonalVRF (final double n, final double tau) {
        DMatrixRMaj V = new DMatrixRMaj(order + 1, order + 1);
                
        //  V = zeros(this.order + 1, this.order + 1)
        CommonOps_DDRM.fill( V, 0.0 );
                
        V.unsafe_set(0, 0, this._getFirstVRF(n, tau));
                
        V.unsafe_set(1, 1, (100.0 * (48.0 * Math.pow(n, 6) + 666.0 * Math.pow(n, 5) + 3843.0 * Math.pow(n, 4) + 11982.0 * Math.pow(n, 3) + 21727.0 * Math.pow(n, 2) + 21938.0 * n + 9516.0)) / (n * Math.pow(tau, 2) * (((Math.pow(n, 8) + 9.0 * Math.pow(n, 7) + 6.0 * Math.pow(n, 6)) - 126.0 * Math.pow(n, 5) - 231.0 * Math.pow(n, 4) + 441.0 * Math.pow(n, 3) + 944.0 * Math.pow(n, 2)) - 324.0 * n - 720.0)));
                
        V.unsafe_set(2, 2, (35280.0 * (9.0 * Math.pow(n, 4) + 76.0 * Math.pow(n, 3) + 239.0 * Math.pow(n, 2) + 336.0 * n + 185.0)) / (n * Math.pow(tau, 4) * (((Math.pow(n, 8) + 9.0 * Math.pow(n, 7) + 6.0 * Math.pow(n, 6)) - 126.0 * Math.pow(n, 5) - 231.0 * Math.pow(n, 4) + 441.0 * Math.pow(n, 3) + 944.0 * Math.pow(n, 2)) - 324.0 * n - 720.0)));
                
        V.unsafe_set(3, 3, (100800.0 * ((n - 3.0) * (n + 5.0) + 63.0 * Math.pow((n + 2.0), 2))) / (n * Math.pow(tau, 6) * (n - 3.0) * (n - 2.0) * (n - 1.0) * (n + 1.0) * (n + 2.0) * (n + 3.0) * (n + 4.0) * (n + 5.0)));
                
        V.unsafe_set(4, 4, this._getLastVRF(n, tau));
        return V;
    }
    
    
    protected DMatrixRMaj _getVRF (final double n, final double tau) {
        DMatrixRMaj V = new DMatrixRMaj(order + 1, order + 1);
                
        V = this._getDiagonalVRF(n, tau);
                
        V.unsafe_set(0, 1, (50.0 * (6.0 * Math.pow(n, 3) + 27.0 * Math.pow(n, 2) + 59.0 * n + 48.0)) / (n * tau * ((Math.pow(n, 4) - 5.0 * Math.pow(n, 3) + 5.0 * Math.pow(n, 2) + 5.0 * n) - 6.0)));
                
        //  V(1, 0) = V(0, 1)
        double     td24 = V.get(0, 1);
        V.unsafe_set(1, 0, td24);
                
        V.unsafe_set(0, 2, (2100.0 * (Math.pow(n, 2) + 3.0 * n + 3.0)) / (n * Math.pow(tau, 2) * ((Math.pow(n, 4) - 5.0 * Math.pow(n, 3) + 5.0 * Math.pow(n, 2) + 5.0 * n) - 6.0)));
                
        //  V(2, 0) = V(0, 2)
        double     td44 = V.get(0, 2);
        V.unsafe_set(2, 0, td44);
                
        V.unsafe_set(0, 3, (4200.0 * (2.0 * n + 3.0)) / (n * Math.pow(tau, 3) * ((Math.pow(n, 4) - 5.0 * Math.pow(n, 3) + 5.0 * Math.pow(n, 2) + 5.0 * n) - 6.0)));
                
        //  V(3, 0) = V(0, 3)
        double     td62 = V.get(0, 3);
        V.unsafe_set(3, 0, td62);
                
        V.unsafe_set(0, 4, 15120.0 / (n * Math.pow(tau, 4) * ((Math.pow(n, 4) - 5.0 * Math.pow(n, 3) + 5.0 * Math.pow(n, 2) + 5.0 * n) - 6.0)));
                
        //  V(4, 0) = V(0, 4)
        double     td77 = V.get(0, 4);
        V.unsafe_set(4, 0, td77);
                
        V.unsafe_set(1, 2, (4200.0 * (9.0 * Math.pow(n, 4) + 84.0 * Math.pow(n, 3) + 295.0 * Math.pow(n, 2) + 467.0 * n + 297.0)) / (n * Math.pow(tau, 3) * (((Math.pow(n, 7) + 7.0 * Math.pow(n, 6)) - 8.0 * Math.pow(n, 5) - 110.0 * Math.pow(n, 4) - 11.0 * Math.pow(n, 3) + 463.0 * Math.pow(n, 2) + 18.0 * n) - 360.0)));
                
        //  V(2, 1) = V(1, 2)
        double     td113 = V.get(1, 2);
        V.unsafe_set(2, 1, td113);
                
        V.unsafe_set(1, 3, (1680.0 * (96.0 * Math.pow(n, 4) + 894.0 * Math.pow(n, 3) + 3191.0 * Math.pow(n, 2) + 5059.0 * n + 2940.0)) / (n * Math.pow(tau, 4) * (((Math.pow(n, 8) + 9.0 * Math.pow(n, 7) + 6.0 * Math.pow(n, 6)) - 126.0 * Math.pow(n, 5) - 231.0 * Math.pow(n, 4) + 441.0 * Math.pow(n, 3) + 944.0 * Math.pow(n, 2)) - 324.0 * n - 720.0)));
                
        //  V(3, 1) = V(1, 3)
        double     td152 = V.get(1, 3);
        V.unsafe_set(3, 1, td152);
                
        V.unsafe_set(1, 4, (151200.0 * (2.0 * Math.pow(n, 2) + 11.0 * n + 19.0)) / (n * Math.pow(tau, 5) * (((Math.pow(n, 7) + 7.0 * Math.pow(n, 6)) - 8.0 * Math.pow(n, 5) - 110.0 * Math.pow(n, 4) - 11.0 * Math.pow(n, 3) + 463.0 * Math.pow(n, 2) + 18.0 * n) - 360.0)));
                
        //  V(4, 1) = V(1, 4)
        double     td182 = V.get(1, 4);
        V.unsafe_set(4, 1, td182);
                
        V.unsafe_set(2, 3, (352800.0 * (4.0 * Math.pow(n, 2) + 17.0 * n + 18.0)) / (n * Math.pow(tau, 5) * (((Math.pow(n, 7) + 7.0 * Math.pow(n, 6)) - 8.0 * Math.pow(n, 5) - 110.0 * Math.pow(n, 4) - 11.0 * Math.pow(n, 3) + 463.0 * Math.pow(n, 2) + 18.0 * n) - 360.0)));
                
        //  V(3, 2) = V(2, 3)
        double     td212 = V.get(2, 3);
        V.unsafe_set(3, 2, td212);
                
        V.unsafe_set(2, 4, (302400.0 * (9.0 * Math.pow(n, 2) + 39.0 * n + 47.0)) / (n * Math.pow(tau, 6) * (((Math.pow(n, 8) + 9.0 * Math.pow(n, 7) + 6.0 * Math.pow(n, 6)) - 126.0 * Math.pow(n, 5) - 231.0 * Math.pow(n, 4) + 441.0 * Math.pow(n, 3) + 944.0 * Math.pow(n, 2)) - 324.0 * n - 720.0)));
                
        //  V(4, 2) = V(2, 4)
        double     td245 = V.get(2, 4);
        V.unsafe_set(4, 2, td245);
                
        V.unsafe_set(3, 4, 12700800.0 / (n * Math.pow(tau, 7) * (n - 3.0) * (n - 2.0) * (n - 1.0) * (n + 1.0) * (n + 3.0) * (n + 4.0) * (n + 5.0)));
                
        //  V(4, 3) = V(3, 4)
        double     td263 = V.get(3, 4);
        V.unsafe_set(4, 3, td263);
        return V;
    }
    
} // class Emp

