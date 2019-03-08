// AbstractRecursiveFilter_test.cpp

#include <iostream>
#include <vector>

#include <cmath>

#include <netcdf.h>
#include <Eigen/Dense>

#include <doctest.h>
#include <TestData.hpp>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>
#include <polynomialfiltering/Main.hpp>
#include <polynomialfiltering/components/AbstractRecursiveFilter.hpp>

using namespace Eigen;
using namespace PolynomialFiltering;

static std::string filename = "AbstractRecursiveFilter.nc";

static int ORDER = 3;

class AbstractRecursiveFilterMock : protected Components::AbstractRecursiveFilter {
public:

	AbstractRecursiveFilterMock(long order, double tau) : AbstractRecursiveFilter(order, tau) {
	}

	RealMatrix testInitialization(RealMatrix setup, RealMatrix data) {
		RealMatrix actual = MatrixXd::Constant(5 + 2 * (this->order + 1), 1, 0.0);
		//[n, n0, t0, t, tau, Z, D]
		actual(0, 0) = this->n;
		actual(1, 0) = this->n0;
		actual(2, 0) = this->t0;
		actual(3, 0) = this->t;
		actual(4, 0) = this->tau;
		actual.block(5, 0, this->order + 1, 1) = this->Z;
		actual.block(5 + this->order + 1, 0, this->order + 1, 1) = this->D;
		return actual;
	}

	RealMatrix testStateManagement(RealMatrix setup, RealMatrix data) {
		double t0 = setup(2);
		double t1 = setup(3);

		start(t0, data.row(0));
		CHECK_EQ(getTime(), t0);

		RealMatrix actual = MatrixXd::Zero(this->order + 1,2);
		std::cout << actual << std::endl;
		std::cout << getState(t0) << std::endl;

		actual.col(0) = getState(t0);
		actual.col(1) = getState(setup(3));
		return actual;
	}

private:
	double gammaParameter(const double t, const double dtau) {
		return 0;
	}
	RealVector gamma(const double nOrT) {
		return Vector3d(1, 2, 3);
	}
};

class TestClass {
public:
	TestData* testData;

	TestClass() {
		testData = new TestData(filename);
	}


};


TEST_CASE_FIXTURE(TestClass, "Abstract Recursive Filter Test") {

	SUBCASE("Initialization") {
		std::vector<std::string> matches = testData->getMatchingGroups("testInitialization");
		for (int i = 0; i < matches.size(); i++) {
			RealMatrix setup = testData->getGroupVariable(matches.at(i), "setup");
			RealMatrix data = testData->getGroupVariable(matches.at(i), "data");
			RealMatrix expected = testData->getGroupVariable(matches.at(i), "expected");

			std::shared_ptr< AbstractRecursiveFilterMock > mock(new AbstractRecursiveFilterMock((long) setup(0), setup(1) ));
			RealMatrix actual = mock->testInitialization(setup, data);

			CHECK(expected.isApprox(actual));
		}
	}

	SUBCASE("State Management") {
		std::vector<std::string> matches = testData->getMatchingGroups("testStateManagement");
		for (int i = 0; i < matches.size(); i++) {
			RealMatrix setup = testData->getGroupVariable(matches.at(i), "setup");
			RealMatrix data = testData->getGroupVariable(matches.at(i), "data");
			RealMatrix expected = testData->getGroupVariable(matches.at(i), "expected");

			std::shared_ptr< AbstractRecursiveFilterMock > mock(new AbstractRecursiveFilterMock((long)setup(0), setup(1)));
			RealMatrix actual = mock->testStateManagement(setup, data);

			CHECK(expected.isApprox(actual));
		}
	}

	std::cout << std::endl;
}