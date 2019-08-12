/***** /components/EMP_test/
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





#pragma float_control(push)
#pragma float_control(precise, off)
namespace polynomialfiltering {
    namespace components {
        namespace EMP_test {
            
            using namespace Eigen;
            
            class RecursivePolynomialFilterMock : public RecursivePolynomialFilter {
                public:
                    RecursivePolynomialFilterMock (const int order, const double tau, const std::shared_ptr<polynomialfiltering::components::ICore> core) : RecursivePolynomialFilter(order,tau,core) {
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
            RealMatrix expected;
            int offset;
            double tau;
            std::shared_ptr<polynomialfiltering::components::ICore> core;
            std::shared_ptr<polynomialfiltering::components::RecursivePolynomialFilter> rf;
            std::shared_ptr<RecursivePolynomialFilterMock> f;
            RealMatrix V;
            RealMatrix E;
            testData = std::make_shared<TestData>("testEMP.nc");
            matches = testData->getMatchingGroups("VRF_");
            assert_not_empty(matches);
            for (int order = 0; order < matches->size(); order++) {
                setup = testData->getGroupVariable(matches[order], "setup");
                N = int(setup(0, 0));
                taus = testData->getGroupVariable(matches[order], "taus");
                expected = testData->getGroupVariable(matches[order], "expected");
                offset = 0;
                for (int itau = 0; itau < taus->size(); itau++) {
                    tau = taus(itau, 0);
                    rf = makeEmp(order, tau);
                    f = this->RecursivePolynomialFilterMock(order, tau, rf->getCore());
                    for (int iN = order + 1; iN < N; iN++) {
                        f->setN(iN + 0);
                        V = f->getVRF();
                        E = expected.block(offset, 0, offset + order + 1 - offset, expected->columns());
                        assert_almost_equal(V, E);
                        offset += order + 1;
                        assert_almost_equal(V(0, 0), f->getFirstVRF());
                        assert_almost_equal(V(V->rows()-1, V->columns()-1), f->getLastVRF());
                        assert_almost_equal(diag(V), diag(f->getDiagonalVRF()));
                    }
                }
            }
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
            std::shared_ptr<polynomialfiltering::components::ICore> core;
            std::shared_ptr<polynomialfiltering::components::RecursivePolynomialFilter> f;
            double e;
            testData = std::make_shared<TestData>("testEMP.nc");
            matches = testData->getMatchingGroups("States");
            assert_not_empty(matches);
            setup = testData->getGroupVariable(matches[0], "setup");
            matches = testData->getMatchingGroups("Case_");
            assert_not_empty(matches);
            for (int i = 0; i < matches->size(); i++) {
                order = int(setup(i, 0));
                tau = setup(i, 1);
                times = testData->getGroupVariable(matches[i], "times");
                observations = testData->getGroupVariable(matches[i], "observations");
                expected = testData->getGroupVariable(matches[i], "expected");
                actual = ArrayXXd::Zero(expected.rows(), expected.cols());
                f = makeEmp(order, tau);
                f->start(0.0, expected.row(0));
                for (int j = 0; j < times.rows(); j++) {
                    Zstar = f->predict(times(j, 0));
                    e = observations(j) - Zstar(0);
                    f->update(times(j, 0), Zstar, e);
                    actual.row(j) = f->getState();
                }
                assert_almost_equal(actual, expected);
            }
        }

        void test9NUnitLastVRF () {
            std::shared_ptr<polynomialfiltering::components::ICore> core;
            double tau;
            RealMatrix taus;
            int n;
            taus = (RealVector5() << 0.01, 0.1, 1., 10., 100.).finished();
            for (int order = 0; order < 5 + 1; order++) {
                for (int itau = 0; itau < taus->size(); itau++) {
                    tau = taus(itau);
                    n = nUnitLastVRF(order, tau);
                    core = _makeEmpCore(order, tau);
                }
            }
        }

        }; // namespace EMP_test
    }; // namespace components
}; // namespace polynomialfiltering

#pragma float_control(pop)

TEST_CASE("EMP_test") {
    SUBCASE("test1CheckVRF") {
        components::EMP_test::test1CheckVRF();
    }
    SUBCASE("test2CheckStates") {
        components::EMP_test::test2CheckStates();
    }
    SUBCASE("test9NUnitLastVRF") {
        components::EMP_test::test9NUnitLastVRF();
    }
}

