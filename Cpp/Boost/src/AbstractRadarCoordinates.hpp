#include <iostream>
#include <math.h>

#include <boost/bind/bind.hpp>
#include "boost/math/special_functions/pow.hpp"
#include <boost/numeric/ublas/lu.hpp>
#include <boost/numeric/ublas/io.hpp>
#include <boost/math/special_functions/factorials.hpp>
#include <boost/tuple/tuple.hpp>

#include "Filtering.hpp"

using namespace boost::math;
using namespace boost::numeric::ublas;

#define POW(a,b) pow(a,b)

class AbstractRadarCoordinates {
public:

	RealMatrix ENU2AER(RealVector E, RealVector N, RealVector U) {
		RealMatrix AER(E.size(), 3);
		AER(0, 0) = fmod(atan2(N(0), E(0)), (2.0*constants::pi<double>()));  // azimuth
		AER(0, 1) = atan2(U(0), sqrt(pow<2>(E(0)) + pow<2>(N(0))));
		AER(0, 2) = sqrt(pow<2>(E(0)) + pow<2>(N(0)) + pow<2>(U(0)));
		return AER;
	};

	RealMatrix AER2ENU(RealVector A, RealVector E, RealVector R) {
		RealMatrix ENU(A.size(), 3);
		ENU(0, 0) = R(0) * cos(E(0)) * sin(A(0));
		ENU(0, 1) = R(0) * cos(E(0)) * cos(A(0));
		ENU(0, 2) = R(0) * sin(E(0));
		return ENU;
	};

protected:
	virtual double d1AzimuthdENU1(const RealVector E, const RealVector N, const RealVector U) = 0;
	virtual double d2AzimuthdENU2(const RealVector E, const RealVector N, const RealVector U) = 0;
	virtual double d3AzimuthdENU3(const RealVector E, const RealVector N, const RealVector U) = 0;
	virtual double d4AzimuthdENU4(const RealVector E, const RealVector N, const RealVector U) = 0;
	virtual double d5AzimuthdENU5(const RealVector E, const RealVector N, const RealVector U) = 0;

	virtual double d1ElevationdENU1(const RealVector E, const RealVector N, const RealVector U) = 0;
	virtual double d2ElevationdENU2(const RealVector E, const RealVector N, const RealVector U) = 0;
	virtual double d3ElevationdENU3(const RealVector E, const RealVector N, const RealVector U) = 0;
	virtual double d4ElevationdENU4(const RealVector E, const RealVector N, const RealVector U) = 0;
	virtual double d5ElevationdENU5(const RealVector E, const RealVector N, const RealVector U) = 0;

	virtual double d1RangedENU1(const RealVector E, const RealVector N, const RealVector U) = 0;
	virtual double d2RangedENU2(const RealVector E, const RealVector N, const RealVector U) = 0;
	virtual double d3RangedENU3(const RealVector E, const RealVector N, const RealVector U) = 0;
	virtual double d4RangedENU4(const RealVector E, const RealVector N, const RealVector U) = 0;
	virtual double d5RangedENU5(const RealVector E, const RealVector N, const RealVector U) = 0;

	virtual double d1EastdAER1(const RealVector A, const RealVector E, const RealVector R) = 0;
	virtual double d2EastdAER2(const RealVector A, const RealVector E, const RealVector R) = 0;
	virtual double d3EastdAER3(const RealVector A, const RealVector E, const RealVector R) = 0;
	virtual double d4EastdAER4(const RealVector A, const RealVector E, const RealVector R) = 0;
	virtual double d5EastdAER5(const RealVector A, const RealVector E, const RealVector R) = 0;

	virtual double d1NorthdAER1(const RealVector A, const RealVector E, const RealVector R) = 0;
	virtual double d2NorthdAER2(const RealVector A, const RealVector E, const RealVector R) = 0;
	virtual double d3NorthdAER3(const RealVector A, const RealVector E, const RealVector R) = 0;
	virtual double d4NorthdAER4(const RealVector A, const RealVector E, const RealVector R) = 0;
	virtual double d5NorthdAER5(const RealVector A, const RealVector E, const RealVector R) = 0;

	virtual double d1UpdAER1(const RealVector A, const RealVector E, const RealVector R) = 0;
	virtual double d2UpdAER2(const RealVector A, const RealVector E, const RealVector R) = 0;
	virtual double d3UpdAER3(const RealVector A, const RealVector E, const RealVector R) = 0;
	virtual double d4UpdAER4(const RealVector A, const RealVector E, const RealVector R) = 0;
	virtual double d5UpdAER5(const RealVector A, const RealVector E, const RealVector R) = 0;

};