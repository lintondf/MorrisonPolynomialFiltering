/***** /polynomialfiltering/filters/RecursivePolynomialFilter/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED Java from Python Reference Implementation
 */

package polynomialfiltering.filters;
 
import java.util.stream.IntStream;
import org.ejml.data.DMatrixRMaj;
import org.ejml.dense.row.CommonOps_DDRM;
import polynomialfiltering.main.FilterStatus;
import polynomialfiltering.main.AbstractFilter;
import polynomialfiltering.main.AbstractFilterWithCovariance;
import static polynomialfiltering.main.Utility.*;
import polynomialfiltering.components.ICore;
import polynomialfiltering.main.Utility.ValueError;

 

///// @class RecursivePolynomialFilter
/// @brief Base class for both expanding and fading polynomial filter and their combinations.
/// 
public class RecursivePolynomialFilter extends AbstractFilter {
    protected  int n; ///<  number of samples
    protected  double dtau; ///<  delta nominal scaled time step
    protected  double t0; ///<  filter start time
    protected  double tau; ///<  nominal scaled time step
    protected  double t; ///<   time of the last input
    protected  DMatrixRMaj Z = new DMatrixRMaj(); ///<  NORMALIZED state vector at time of last input
    protected  DMatrixRMaj D = new DMatrixRMaj(); ///<  noralization/denormalization scaling vector; D(tau) = [tau^-0, tau^-1,...tau^-order]
    protected  ICore core; ///<  provider of core expanding / fading functions
    
    public RecursivePolynomialFilter() {}  // auto-generated null constructor


    ///// @brief Constructor
    /// 
    /// 
    ///  @param		order	integer polynomial orer
    ///  @param		tau	nominal time step
    /// 
    
    public RecursivePolynomialFilter (final int order, final double tau, final ICore core) {
        super(order);
        double td; ///<  tau^d 
        if (order < 0 || order > 5) {
            throw new ValueError("Polynomial orders < 0 or > 5 are not supported");
        }
                
        this.n = 0;
        this.core = core;
                
        this.dtau = 0;
                
        this.t0 = 0;
                
        this.t = 0;
                
        //  this.Z = zeros(this.order + 1)
        this.Z.reshape(this.order + 1, 1);
        CommonOps_DDRM.fill( this.Z, 0.0 );
                
        this.tau = tau;
                
        //  this.D = zeros(this.order + 1)
        this.D.reshape(this.order + 1, 1);
        CommonOps_DDRM.fill( this.D, 0.0 );
        for (int d = 0; d < this.order + 1; d++) {
                        
            td = Math.pow(this.tau, d);
                        
            this.D.unsafe_set(0, d, td);
        }
    }
    

    ///// @brief Estimate of the FMP fading factor theta to match 0th variance of an EMP
    /// 
    /// 
    ///  @param		order	integer polynomial order
    ///  @param		n	float sample number
    /// 
    
    static public double effectiveTheta (final int order, final double n) {
        double factor;
        if (n < 1) {
            return 0.0;
        }
                
        factor = 1.148 * order + 2.0367;
        return 1.0 - factor / n;
    }
    

    ///// @brief Copy the state of another filter into this filter.
    /// 
    
    public void copyState (final RecursivePolynomialFilter that) {
        this.n = that.n;
        this.t0 = that.t0;
        this.t = that.t;
        this.tau = that.tau;
        this.D = that.D;
        this.Z = that.Z;
    }
    
    
    public void add(final double t, final double y) {
        add(t, y, -1);
    }
    
    public void add (final double t, final double y, final int observationId) {
        DMatrixRMaj Zstar = new DMatrixRMaj();
        double e;
                
        Zstar = this.predict(t);
                
        //  e = y - Zstar(0)
        double     td2 = Zstar.get(0);
        e = y - td2;
                
        DMatrixRMaj tm4 = this.update(t, Zstar, e);
    }
    

    ///// @brief Start or restart the filter
    /// 
    /// 
    ///  @param		t	external start time
    ///  @param		Z	state vector in external units
    /// 
    ///  @return   @return		None
    /// 
    /// 
    
    public void start (final double t, final DMatrixRMaj Z) {
                
        this.n = 0;
                
        this.t0 = t;
                
        this.t = t;
                
        //  this.Z = this._normalizeState(this._conformState(Z))
        DMatrixRMaj tm1 = this._conformState(Z);
        this.Z = this._normalizeState(tm1);
    }
    

    ///// @brief Predict the filter state (Z*) at time t
    /// 
    /// 
    ///  @param		t	target time
    /// 
    ///  @return  predicted state INTERNAL UNITS
    /// 
    /// 
    
    public DMatrixRMaj predict (final double t) {
        DMatrixRMaj Zstar = new DMatrixRMaj(order+1, 1);
        double dt;
        double dtau;
        DMatrixRMaj F = new DMatrixRMaj(order+1, order+1);
                
        dt = t - this.t;
                
        dtau = this._normalizeDeltaTime(dt);
                
        F = RecursivePolynomialFilter.stateTransitionMatrix(this.order + 1, dtau);
                
        //  Zstar = F * this.Z
        CommonOps_DDRM.mult( F, this.Z, Zstar );
        return Zstar;
    }
    

    ///// @brief Update the filter state from using the prediction error e
    /// 
    /// 
    ///  @param		t	update time
    ///  @param		Zstar	predicted NORMALIZED state at update time
    ///  @param		e	prediction error (observation - predicted state)
    /// 
    ///  @return  innovation vector
    /// 
    ///  @par Examples
    /// Zstar = self.predict(t)
    /// e = observation[0] - Zstar[0]
    /// self.update(t, Zstar, e )
    /// 
    
    public DMatrixRMaj update (final double t, final DMatrixRMaj Zstar, final double e) {
        double dt;
        double dtau;
        DMatrixRMaj gamma = new DMatrixRMaj(order+1, 1);
        DMatrixRMaj innovation = new DMatrixRMaj(order+1, 1);
                
        dt = t - this.t;
                
        dtau = this._normalizeDeltaTime(dt);
        gamma = this.core.getGamma(this._normalizeTime(t), dtau);
                
        //  innovation = gamma * e
        CommonOps_DDRM.scale( e, gamma, innovation );
                
        //  this.Z = (Zstar + innovation)
        this.Z.reshape( Zstar.numRows, Zstar.numCols );
        CommonOps_DDRM.add( Zstar, innovation, this.Z );
                
        this.t = t;
        this.n += 1;
        if (this.n < this.core.getSamplesToStart()) {
            this.setStatus(FilterStatus.INITIALIZING);
        } else {
            this.setStatus(FilterStatus.RUNNING);
        }
        return innovation;
    }
    
    
    public ICore getCore () {
        ICore _getCore_return_value; ///< auto-generated return variable
        _getCore_return_value = this.core;
        return _getCore_return_value;
    }
    

    ///// @brief Return the number of processed observations since start
    /// 
    /// 
    ///  @param		None
    /// 
    ///  @return  Count of processed observations
    /// 
    /// 
    
    public int getN () {
        return this.n;
    }
    

    ///// @brief Return the nominal time step for the filter
    /// 
    /// 
    ///  @param		None
    /// 
    ///  @return  Nominal time step (tau) in external units
    /// 
    /// 
    
    public double getTau () {
        return this.tau;
    }
    

    ///// @brief Return the time of the last processed observation or filter start
    /// 
    /// 
    ///  @param		None
    /// 
    ///  @return  Time in external units
    /// 
    /// 
    
    public double getTime () {
        return this.t;
    }
    

    ///// @brief Get the current filter state vector
    /// 
    /// 
    ///  @param		None
    /// 
    ///  @return  State vector in external units
    /// 
    /// 
    
    public DMatrixRMaj getState () {
        
        return  this._denormalizeState(this.Z);
    }
    
    
    public double getFirstVRF () {
        if (this.n < this.core.getSamplesToStart()) {
            return 0.0;
        }
        return this.core.getFirstVRF(this.n);
    }
    
    
    public double getLastVRF () {
        if (this.n < this.core.getSamplesToStart()) {
            return 0.0;
        }
        return this.core.getLastVRF(this.n);
    }
    

    ///// @brief Get the variance reduction factor matrix
    /// 
    /// 
    ///  @param		None
    /// 
    ///  @return  Square matrix (order+1) of input to output variance ratios
    /// 
    /// 
    
    public DMatrixRMaj getVRF () {
        DMatrixRMaj V = new DMatrixRMaj(order+1, order+1);
        if (this.n < this.order + 1) {
                        
            //  V = zeros(this.order + 1, this.order + 1)
            CommonOps_DDRM.fill( V, 0.0 );
            return V;
        }
        V = this.core.getVRF(this.n);
        return V;
    }
    

    ///// @brief Matches an input state vector to the filter order
    /// 
    /// Longer state vectors are truncated and short ones are zero filled
    /// 
    /// 
    ///  @param		state	arbitrary length input state vector
    /// 
    ///  @return  conformed state vector with order+1 elements
    /// 
    /// 
    
    protected DMatrixRMaj _conformState (final DMatrixRMaj state) {
        DMatrixRMaj Z = new DMatrixRMaj();
        
        //  asssignment.dummy = return ( AbstractFilter.conformState(this.order, state))
        DMatrixRMaj tm3 = AbstractFilter.conformState(this.order, state);
        return tm3;
    }
    

    ///// @brief Convert an external time to internal (tau) units
    /// 
    /// 
    ///  @param		t	external time (e.g. seconds)
    /// 
    ///  @return  time in internal units (tau steps since t0)
    /// 
    /// 
    
    protected double _normalizeTime (final double t) {
        return (t - this.t0) / this.tau;
    }
    

    ///// @brief Converts external delta time to internal (tau) step units
    /// 
    /// 
    ///  @param		dt	external time step (e.g. seconds)
    /// 
    ///  @return  time step in internal units
    /// 
    /// 
    
    protected double _normalizeDeltaTime (final double dt) {
        return dt / this.tau;
    }
    

    ///// @brief Normalize a state vector
    /// 
    /// Multiplies the input state vector by the normalization vector D
    /// 
    /// 
    ///  @param		Z	state vector in external units
    /// 
    ///  @return  state vector in internal units
    /// 
    /// 
    
    protected DMatrixRMaj _normalizeState (final DMatrixRMaj Z) {
        DMatrixRMaj R = new DMatrixRMaj(order+1, 1);
                
        //  R = Z .* this.D
        CommonOps_DDRM.elementMult( Z, this.D, R );
        return R;
    }
    

    ///// @brief Denormalize a state vector
    /// 
    /// Divides the input state vector by the normalization vector D
    /// 
    /// 
    ///  @param		Z	state vector in internal units
    /// 
    ///  @return  state vector in external units
    /// 
    /// 
    
    protected DMatrixRMaj _denormalizeState (final DMatrixRMaj Z) {
        DMatrixRMaj R = new DMatrixRMaj(order+1, 1);
                
        //  R = Z ./ this.D
        CommonOps_DDRM.elementDiv( Z, this.D, R );
        return R;
    }
    
} // class filters

