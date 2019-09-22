/***** /polynomialfiltering/Main/FilterStatus/
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

 

///// @class FilterStatus
/// @brief The FilterStats enumeration defines the possible states of a filter.
/// 
///  	IDLE	Filter is awaiting the first observation
///  	INITIALIZING	Filter has processed one or more observations, but status estimate is not reliable
///  	RUNNING	Filter status estimate is reliable
///  	COASTING	Filter has not received a recent observation, but the predicted status should be usable
///  	RESETING	Filter coast interval has been exceed and it will reinitialize on the next observation
/// 
public enum FilterStatus {
    IDLE,
    INITIALIZING,
    RUNNING,
    COASTING,
    RESETING,
} // class Main

