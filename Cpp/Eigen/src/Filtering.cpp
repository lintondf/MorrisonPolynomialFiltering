#include <iostream>

#include <boost/bind/bind.hpp>
#include <boost/math/special_functions/pow.hpp>
#include <boost/numeric/ublas/lu.hpp>
#include <boost/numeric/ublas/io.hpp>
#include <boost/math/special_functions/factorials.hpp>
#include <boost/accumulators/accumulators.hpp>
#include <boost/accumulators/statistics/stats.hpp>
#include <boost/accumulators/statistics/mean.hpp>
#include <boost/accumulators/statistics/variance.hpp>
#include <boost/accumulators/statistics/moment.hpp>

#include "Filtering.hpp"

#include "RadarCoordinatesTemplate.hpp"

using namespace boost::accumulators;

using namespace boost::numeric::ublas;
using namespace boost::tuples;

matrix<double> stateTransitionMatrix(const std::size_t N, double dt) {
	matrix<double> B = identity_matrix<double>(N);
	for (std::size_t i = 0; i < N; i++) {
		for (std::size_t j = i + 1; j < N; j++) {
			unsigned ji = (unsigned) (j - i);
			double fji = boost::math::factorial<double>(ji);
			B(i, j) = pow(dt, ji) / fji;
		}
	}
	return B;
}





int main() {
	using namespace boost::numeric::ublas;

	std::cout << boost::math::pow<3>(10) << std::endl;

	/*
	matrix<double> TntTn(3,3);
	TntTn(0, 0) = 11.0; TntTn(0, 1) = -5.5; TntTn(0, 2) = 3.85;
	TntTn(1, 0) = -5.5; TntTn(1, 1) = 3.85; TntTn(1, 2) = -3.025;
	TntTn(2, 0) = 3.85; TntTn(2, 1) = -3.025; TntTn(2, 2) = 2.5333;
	vector<double> TntYn(3);
	TntYn(0) = 45.99012356;
	TntYn(1) = -9.88611426;
	TntYn(2) = 0.36213461;

	std::cout << TntTn << std::endl;
	std::cout << TntYn << std::endl;

	permutation_matrix<std::size_t> pm(TntTn.size1());
	lu_factorize(TntTn, pm); 
	lu_substitute(TntTn, pm, TntYn);
	std::cout << TntYn << std::endl;

	std::cout << stateTransitionMatrix(8, 0.1) << std::endl;
	*/
	RadarCoordinates rc;

	RealVector E(1), N(1), U(1);
	E(0) = 10;
	N(0) = 20;
	U(0) = 50;
	std::cout << rc.ENU2AER(E, N, U) << std::endl;
	return 0;
}

