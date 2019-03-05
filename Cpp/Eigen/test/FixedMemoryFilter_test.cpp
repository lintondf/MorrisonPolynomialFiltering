// FixedMemoryFilter_test.cpp

#include <iostream>
#include <vector>

#include <cmath>

#include <netcdf.h>
#include <Eigen/Dense>

#include <doctest.h>
#include <TestData.hpp>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>
#include <polynomialfiltering/Main.hpp>
#include <polynomialfiltering/components/FixedMemoryPolynomialFilter.hpp>

using namespace Eigen;
using namespace PolynomialFiltering;


#define FILE_NAME 

RealMatrix executePerfect(RealMatrix setup, RealMatrix data) {
	int order = (int)setup(0);
	int window = (int)setup(1);
	int M = (int)setup(2);
	int iCheck = (int)setup(3);
	
	RealMatrix times = data.col(0);
	RealMatrix observations = data.col(1);

	Components::FixedMemoryFilter fixed(order, window);
	for (int i = 0; i < M; i++) {
		fixed.add( times(i), observations(i) );
	}
	return fixed.getState(times(iCheck));
}

TestData* testData;

TEST_CASE("Fixed Memory Polynomial Filter Test") {
	testData = new TestData("FixedMemoryFiltering.nc");

	SUBCASE("Perfect Data Endpoint Test") {
		std::vector<std::string> matches = testData->getMatchingGroups("testPerfect");
		for (int i = 0; i < matches.size(); i++) {
			RealMatrix setup = testData->getGroupVariable(matches.at(i), "setup");
			RealMatrix data = testData->getGroupVariable(matches.at(i), "data");
			RealMatrix expected = testData->getGroupVariable(matches.at(i), "expected");

			RealMatrix actual = executePerfect(setup, data);
			CHECK(expected.isApprox(expected));
		}
	}

	delete testData;
}
