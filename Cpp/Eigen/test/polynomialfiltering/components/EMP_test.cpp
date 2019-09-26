/***** /polynomialfiltering/components/EMP_test/
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
#include <TestData.hpp>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>


#include <TestData.hpp>
#include <polynomialfiltering/filters/RecursivePolynomialFilter.hpp>
#include <polynomialfiltering/Main.hpp>
#include <polynomialfiltering/components/ICore.hpp>
#include <polynomialfiltering/components/Emp.hpp>
#include <TestData.hpp>




#pragma float_control(push)
#pragma float_control(precise, off)
    namespace polynomialfiltering {
        namespace components {
            
            using namespace Eigen;
            
            class EMP_test {
            public:
                class RecursivePolynomialFilterMock : public RecursivePolynomialFilter {
                    public:
                        RecursivePolynomialFilterMock (const int order, const double tau, const std::shared_ptr<ICore> core) : RecursivePolynomialFilter(order,tau,core) {
                        }

                        void setN (const int n) {
                            this->n = n;
                        }

                }; // class RecursivePolynomialFilterMock 

            void test1CheckVRF () {
                std::shared_ptr<TestData> testData;
                std::vector<std::string> matches;
                RealMatrix setup;
                int N;
                RealMatrix taus;
                int nTaus;
                RealMatrix expected;
                int offset;
                double tau;
                std::shared_ptr<ICore> core;
                std::shared_ptr<filters::RecursivePolynomialFilter> rf;
                std::shared_ptr<RecursivePolynomialFilterMock> f;
                RealMatrix V;
                RealMatrix E;
                assert_clear();
                testData = std::make_shared<TestData>("testEMP.nc");
                matches = testData->getMatchingGroups("VRF_");
                assert_not_empty(matches);
                for (int order = 0; order < matches.size(); order++) {
                    setup = testData->getGroupVariable(matches[order], "setup");
                    N = int(setup(0));
                    taus = testData->getGroupVariable(matches[order], "taus");
                    expected = testData->getGroupVariable(matches[order], "expected");
                    offset = 0;
                    nTaus = taus.size();
                    for (int itau = 0; itau < nTaus; itau++) {
                        tau = taus(itau);
                        rf = Emp::makeEmp(order, tau);
                        f = std::make_shared<RecursivePolynomialFilterMock>(order, tau, rf->getCore());
                        for (int iN = order + 1; iN < N; iN++) {
                            f->setN(iN + 0);
                            V = f->getVRF();
                            E = expected.block(offset, 0, offset + order + 1 - offset, expected.cols());
                            assert_almost_equal(V, E);
                            offset += order + 1;
                        }
                    }
                }
                testData->close();
                assertGreaterEqual(2.0, assert_report("Emp_test/test1CheckVRF"));
            }

            void test2CheckStates () {
                std::shared_ptr<TestData> testData;
                std::vector<std::string> matches;
                int order;
                RealMatrix setup;
                RealMatrix taus;
                RealMatrix expected;
                RealMatrix actual;
                RealMatrix times;
                RealMatrix observations;
                RealMatrix Zstar;
                RealMatrix diff;
                double tau;
                std::shared_ptr<ICore> core;
                std::shared_ptr<filters::RecursivePolynomialFilter> f;
                double e;
                assert_clear();
                testData = std::make_shared<TestData>("testEMP.nc");
                matches = testData->getMatchingGroups("States");
                assert_not_empty(matches);
                setup = testData->getGroupVariable(matches[0], "setup");
                matches = testData->getMatchingGroups("States_Case_");
                assert_not_empty(matches);
                for (int i = 0; i < matches.size(); i++) {
                    order = int(setup(i, 0));
                    tau = setup(i, 1);
                    times = testData->getGroupVariable(matches[i], "times");
                    observations = testData->getGroupVariable(matches[i], "observations");
                    expected = testData->getGroupVariable(matches[i], "expected");
                    actual = ArrayXXd::Zero(expected.rows(), expected.cols());
                    f = Emp::makeEmp(order, tau);
                    f->start(0.0, expected.row(0));
                    for (int j = 0; j < times.rows(); j++) {
                        Zstar = f->predict(times(j, 0));
                        e = observations(j) - Zstar(0);
                        f->update(times(j, 0), Zstar, e);
                        actual.row(j) = transpose(f->getState());
                    }
                    assert_almost_equal(actual, expected);
                }
                testData->close();
                assertGreaterEqual(29.2, assert_report("Emp_test/test2CheckStates"));
            }

            void test9NUnitLastVRF () {
                std::shared_ptr<ICore> core;
                double tau;
                RealMatrix taus;
                int nTaus;
                int n;
                taus = (RealVector5() << 0.01, 0.1, 1., 10., 100.).finished();
                for (int order = 0; order < 5 + 1; order++) {
                    nTaus = taus.size();
                    for (int itau = 0; itau < nTaus; itau++) {
                        tau = taus(itau);
                        n = Emp::nUnitLastVRF(order, tau);
                        core = Emp::makeEmpCore(order, tau);
                    }
                }
            }

            void test9Coverage () {
                assertEqual(0.0, Emp::nSwitch(0, 2.0));
            }

            }; // class EMP_test
        }; // namespace components
    }; // namespace polynomialfiltering

#pragma float_control(pop)

TEST_CASE("EMP_test") {
    polynomialfiltering::components::EMP_test test;

    SUBCASE("test1CheckVRF") {
        test.test1CheckVRF();
    }
    SUBCASE("test2CheckStates") {
        test.test2CheckStates();
    }
    SUBCASE("test9NUnitLastVRF") {
        test.test9NUnitLastVRF();
    }
    SUBCASE("test9Coverage") {
        test.test9Coverage();
    }
}

