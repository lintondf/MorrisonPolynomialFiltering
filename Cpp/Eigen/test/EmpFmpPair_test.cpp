// EmpFmpPair_test.cpp

#include <iostream>
#include <vector>
#include <cmath>
#include <netcdf.h>

#include <doctest.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>
#include <polynomialfiltering/Main.hpp>
#include <polynomialfiltering/components/EmpFmpPair.hpp>

#include <TestData.hpp>


using namespace Eigen;
using namespace polynomialfiltering;

static std::string filename = "EmpFmpPair.nc";

static RealMatrix runCase(long order, double theta, double tau, long N, RealMatrix data) {
	components::EmpFmpPair fmp(order, theta, tau);
	RealMatrix actual = zeros(N, order + 1);
	actual.block(0, 0, 1, order + 1) = data.block(0, 2, 1, order + 1);
	//std::cout << " time = " << data(0, 0) << std::endl << " state = " << data.block(0, 2, 1, order + 1) << std::endl;
	RealVector state = data.block(0, 2, 1, order + 1).transpose();
	fmp.start(data(0, 0), state);
	for (int i = 1; i < N; i++) {
		RealVector Z = fmp.predict(data(i, 0));
		double e = data(i, 1) - Z(0);
		fmp.update(data(i, 0), Z, e);
		//std::cout << i << " " << fmp->getState(fmp->getTime()) << std::endl;
		actual.block(i, 0, 1, order + 1) = fmp.getState().transpose();
	}
	return actual;
}

TEST_CASE("EmpFmpPair Test") {
	std::shared_ptr <TestData> testData = TestData::make(filename);
	std::vector<std::string> matches = testData->getMatchingGroups("EmpFmpPair");
	for (int i = 0; i < matches.size(); i++) {
		RealMatrix setup = testData->getGroupVariable(matches.at(i), "setup");
		RealMatrix data = testData->getGroupVariable(matches.at(i), "data");
		RealMatrix expected = testData->getGroupVariable(matches.at(i), "expected");

		int order = (int)setup(0);
		double theta = setup(1);
		double tau = setup(2);
		int N = (int)setup(3);
		double R = setup(4);

		RealMatrix actual = runCase(order, theta, tau, N, data);

		if (!actual.isApprox(expected)) {
			std::cout << "diff" << std::endl;
			std::cout << expected - actual << std::endl;
		}
		CHECK(actual.isApprox(expected));
	}
}