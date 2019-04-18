// EMP_test.cpp

#include <iostream>
#include <vector>
#include <cmath>
#include <netcdf.h>

#include <doctest.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>
#include <polynomialfiltering/Main.hpp>
#include <polynomialfiltering/components/ExpandingMemoryPolynomialFilter.hpp>

#include <TestData.hpp>


using namespace Eigen;
using namespace polynomialfiltering;

static std::string filename = "ExpandingMemoryFiltering.nc";

RealMatrix runCase(long order, double tau, long N, RealMatrix data ) {
	std::shared_ptr<components::EMPBase> emp = components::makeEMP(order, tau);
	RealMatrix actual = zeros(N, order + 1);
	actual.block(0, 0, 1, order + 1) = data.block(0, 2, 1, order + 1);
	//std::cout << " time = " << data(0, 0) << std::endl << " state = " << data.block(0, 2, 1, order + 1) << std::endl;
	RealVector state = data.block(0, 2, 1, order + 1).transpose();
	emp->start(data(0, 0), state);
	for (int i = 1; i < N; i++) {
		RealVector Z = emp->predict(data(i, 0));
		double e = data(i, 1) - Z(0);
		emp->update(data(i, 0), Z, e);
		//std::cout << i << " " << emp->getState(emp->getTime()) << std::endl;
		actual.block(i, 0, 1, order + 1) = emp->getState().transpose();
	}
	return actual;
}

TEST_CASE("Expanding Memory Polynomial Filter Test") {
	INFO("EMP TEST");
	SUBCASE("Perfect Test") {
		std::shared_ptr <TestData> testData = TestData::make(filename);
		std::vector<std::string> matches = testData->getMatchingGroups("testEMPPerfect");
		for (int i = 0; i < matches.size(); i++) {
			RealMatrix setup = testData->getGroupVariable(matches.at(i), "setup");
			RealMatrix data = testData->getGroupVariable(matches.at(i), "data");
			RealMatrix expected = testData->getGroupVariable(matches.at(i), "expected");

			int order = (int)setup(0);
			double tau = setup(1);
			int N = (int)setup(2);
			double R = setup(3);

			RealMatrix actual = runCase(order, tau, N, data);

			////std::cout << "data=" <<std::endl << data << std::endl;

			////std::cout << order << " " << tau << " " << N << " " << data.cols() << std::endl;

			//std::shared_ptr<Components::EMPBase> emp = Components::makeEMP(order, tau);
			//RealMatrix actual = zeros(N, order + 1);
			//actual.block(0, 0, 1, order + 1) = data.block(0, 2, 1, order + 1);
			////std::cout << " time = " << data(0, 0) << std::endl << " state = " << data.block(0, 2, 1, order + 1) << std::endl;
			//RealVector state = data.block(0, 2, 1, order + 1).transpose();
			//emp->start(data(0, 0), state);
			//for (int i = 1; i < N; i++) {
			//	RealVector Z = emp->predict(data(i, 0));
			//	double e = data(i, 1) - Z(0);
			//	emp->update(data(i, 0), Z, e);
			//	//std::cout << i << " " << emp->getState(emp->getTime()) << std::endl;
			//	actual.block(i, 0, 1, order + 1) = emp->getState(emp->getTime()).transpose();
			//}
			if (!actual.isApprox(expected)) {
				std::cout << "diff" << std::endl;
				std::cout << expected-actual << std::endl;
			}
			CHECK(actual.isApprox(expected));
		}
	}

	SUBCASE("Full Suite Test") {
		INFO("Full Suite Test");
		std::shared_ptr <TestData> testData = TestData::make(filename);
		std::vector<std::string> matches = testData->getMatchingGroups("EMPFullSuite");
		for (int i = 0; i < matches.size(); i++) {
			RealMatrix setup = testData->getGroupVariable(matches.at(i), "setup");
			RealMatrix data = testData->getGroupVariable(matches.at(i), "data");
			RealMatrix expected = testData->getGroupVariable(matches.at(i), "expected");

			int order = (int)setup(0);
			double tau = setup(1);
			int N = (int)setup(2);
			double R = setup(3);

			RealMatrix actual = runCase(order, tau, N, data);

			////std::cout << order << " " << tau << " " << N << std::endl;

			//std::shared_ptr<Components::EMPBase> emp = Components::makeEMP(order, tau);
			//RealMatrix actual = zeros(N, order+1);
			//actual.block(0, 0, 1, order + 1) = data.block(0, 2, 1, order + 1);
			////std::cout << "data " << data.rows() << "," << data.cols() << std::endl;
			//emp->start(data(0, 0), data.block(0, 2, 1, order+1).transpose());
			//for (int i = 1; i < N; i++) {
			//	RealVector Z = emp->predict(data(i, 0));
			//	double e = data(i, 1) - Z(0);
			//	emp->update(data(i, 0), Z, e);
			//	actual.block(i, 0, 1, order + 1) = emp->getState(emp->getTime()).transpose();
			//}
			if (!actual.isApprox(expected)) {
				std::cout << actual - expected << std::endl;
			}
			CHECK(actual.isApprox(expected, 1e-10));
		}
	}
}