// FixedMemoryFilter_test.cpp

#include <iostream>
#include <vector>
#include <cmath>
#include <netcdf.h>

#include <doctest.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>
#include <polynomialfiltering/Main.hpp>
#include <polynomialfiltering/components/FixedMemoryPolynomialFilter.hpp>

#include <TestData.hpp>

using namespace Eigen;
using namespace PolynomialFiltering;

static std::string filename = "FixedMemoryFiltering.nc";

class TestDataFixture {
private:
	static TestData* testData;

public:
	TestDataFixture() {
		testData = new TestData(filename);
	}

protected:
	TestData* getTestData() {
		return testData;
	}
};

TestData* TestDataFixture::testData = NULL;

RealMatrix executeEstimatedState(RealMatrix setup, RealMatrix data) {
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

RealMatrix executeVRF(RealMatrix setup, RealMatrix data) {
	int order = (int)setup(0);
	int window = (int)setup(1);
	int M = (int)setup(2);
	int iCheck = (int)setup(3);

	RealMatrix times = data.col(0);
	RealMatrix observations = data.col(1);

	Components::FixedMemoryFilter fixed(order, window);
	for (int i = 0; i < M; i++) {
		fixed.add(times(i), observations(i));
	}
	return fixed.getVRF();
}




TEST_CASE_FIXTURE(TestDataFixture, "Fixed Memory Polynomial Filter Test") {
	SUBCASE("Perfect Data Endpoint Test") {
		TestData* testData = getTestData();
		std::vector<std::string> matches = testData->getMatchingGroups("testPerfect");
		for (int i = 0; i < matches.size(); i++) {
			RealMatrix setup = testData->getGroupVariable(matches.at(i), "setup");
			RealMatrix data = testData->getGroupVariable(matches.at(i), "data");
			RealMatrix expected = testData->getGroupVariable(matches.at(i), "expected");

			RealMatrix actual = executeEstimatedState(setup, data);

			CHECK(expected.isApprox(expected));
		}
	}
}


TEST_CASE_FIXTURE(TestDataFixture, "Fixed Memory Polynomial Filter Test") {
	SUBCASE("Noisy Data Endpoint Test") {
		TestData* testData = getTestData();
		std::vector<std::string> matches = testData->getMatchingGroups("testNoisy");
		for (int i = 0; i < matches.size(); i++) {
			RealMatrix setup = testData->getGroupVariable(matches.at(i), "setup");
			RealMatrix data = testData->getGroupVariable(matches.at(i), "data");
			RealMatrix expected = testData->getGroupVariable(matches.at(i), "expected");

			RealMatrix actual = executeEstimatedState(setup, data);

			CHECK(expected.isApprox(expected));
		}
	}
}

TEST_CASE_FIXTURE(TestDataFixture, "Fixed Memory Polynomial Filter Test") {
	TestData* testData = getTestData();
	SUBCASE("Perfect Data Midpoint Test") {
		std::vector<std::string> matches = testData->getMatchingGroups("testMidpoint");
		for (int i = 0; i < matches.size(); i++) {
			RealMatrix setup = testData->getGroupVariable(matches.at(i), "setup");
			RealMatrix data = testData->getGroupVariable(matches.at(i), "data");
			RealMatrix expected = testData->getGroupVariable(matches.at(i), "expected");

			RealMatrix actual = executeEstimatedState(setup, data);

			CHECK(expected.isApprox(expected));
		}
	}

	delete testData;
}


TEST_CASE_FIXTURE(TestDataFixture, "Fixed Memory Polynomial Filter Test") {
	TestData* testData = getTestData();
	SUBCASE("Variance Reduction Factor Matrix") {
		std::vector<std::string> matches = testData->getMatchingGroups("testVRF");
		for (int i = 0; i < matches.size(); i++) {
			RealMatrix setup = testData->getGroupVariable(matches.at(i), "setup");
			RealMatrix data = testData->getGroupVariable(matches.at(i), "data");
			RealMatrix expected = testData->getGroupVariable(matches.at(i), "expected");

			RealMatrix actual = executeVRF(setup, data);

			CHECK(expected.isApprox(expected));
		}
	}
}
