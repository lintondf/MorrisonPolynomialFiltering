/***** /components/RecursivePolynomialFilter_test/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++ TEST from Python Reference Implementation
 */

#include <iostream>
#include <vector>
#include <cmath>
#include <netcdf.h>

#include <doctest.h>

#include <math.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <TestData.hpp>
#include <polynomialfiltering/components/RecursivePolynomialFilter.hpp>




#pragma float_control(push)
#pragma float_control(precise, off)
namespace polynomialfiltering {
    namespace components {
        namespace RecursivePolynomialFilter_test {
            
            using namespace Eigen;
            
            class PurePredictCore : public ICore {
                public:
                    PurePredictCore (const int order) {
                        this->order = order;
                    }

                    RealVector getGamma (const double t, const double dtau) {
                        RealVector g;
                        g = ArrayXd::Zero(this->order + 1);
                        return g;
                    }

                    RealMatrix getVRF (const int n) {
                        return ArrayXXd::Zero(this->order + 1, this->order + 1);
                    }

                    double getFirstVRF (const int n) {
                        return 0.0;
                    }

                    double getLastVRF (const int n) {
                        return 0.0;
                    }

                    RealMatrix getDiagonalVRF (const int n) {
                        return ArrayXXd::Zero(this->order + 1, this->order + 1);
                    }

                protected:
                    int order;
            }; // class PurePredictCore 

        void test1PurePredict () {
            std::shared_ptr<TestData> testData;
            std::vector<std::string> matches;
            int N;
            int order;
            double tau;
            RealMatrix setup;
            RealMatrix times;
            RealMatrix truth;
            RealMatrix observations;
            RealMatrix actual;
            RealMatrix expected;
            std::shared_ptr<polynomialfiltering::components::ICore> core;
            std::shared_ptr<polynomialfiltering::components::RecursivePolynomialFilter> f;
            RealVector Zstar;
            double e;
            RealMatrix V;
            testData = std::make_shared<TestData>("testRecursivePolynomialFilter.nc");
            matches = testData->getMatchingGroups("testPurePredict_");
            assert_not_empty(matches);
            for (int iMatch = 0; iMatch < matches->size(); iMatch++) {
                setup = testData->getGroupVariable(matches[iMatch], "setup");
                times = testData->getGroupVariable(matches[iMatch], "times");
                truth = testData->getGroupVariable(matches[iMatch], "truth");
                observations = testData->getGroupVariable(matches[iMatch], "observations");
                N = int(setup(0));
                order = int(setup(1));
                tau = setup(2);
                actual = ArrayXXd::Zero(N, order + 1);
                actual.row(0) = truth.row(0);
                core = std::make_shared<RecursivePolynomialFilter_test::PurePredictCore>(order);
                f = std::make_shared<polynomialfiltering::components::RecursivePolynomialFilter>(order, tau, core);
                f->start(times(0), truth.row(0));
                for (int i = 1; i < N; i++) {
                    Zstar = f->predict(times(i));
                    e = observations(i) - Zstar(0);
                    f->update(times(i), Zstar, e);
                    actual.row(i) = f->getState();
                    V = f->getVRF();
                    assert_almost_equal(V, zeros(order + 1, order + 1));
                }
                expected = testData->getGroupVariable(matches[iMatch], "expected");
                assert_almost_equal(actual, expected);
            }
            testData->close();
        }

        }; // namespace RecursivePolynomialFilter_test
    }; // namespace components
}; // namespace polynomialfiltering

#pragma float_control(pop)

TEST_CASE("RecursivePolynomialFilter_test") {
    SUBCASE("test1PurePredict") {
        components::RecursivePolynomialFilter_test::test1PurePredict();
    }
}

