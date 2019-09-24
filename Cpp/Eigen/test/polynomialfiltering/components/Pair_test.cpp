/***** /polynomialfiltering/components/Pair_test/
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
#include <polynomialfiltering/components/RecursivePolynomialFilter.hpp>
#include <polynomialfiltering/Main.hpp>
#include <polynomialfiltering/components/ICore.hpp>
#include <polynomialfiltering/components/Emp.hpp>
#include <polynomialfiltering/components/Fmp.hpp>
#include <polynomialfiltering/components/PairedPolynomialFilter.hpp>
#include <TestData.hpp>




#pragma float_control(push)
#pragma float_control(precise, off)
    namespace polynomialfiltering {
        namespace components {
            
            using namespace Eigen;
            
            class Pair_test {
            public:
                void test2CheckStates () {
                    std::shared_ptr<TestData> testData;
                    Group states;
                    Group caseGroup;
                    std::vector<std::string> matches;
                    int order;
                    double tau;
                    double theta;
                    int nS;
                    int N;
                    RealMatrix times;
                    RealMatrix observations;
                    RealMatrix expectedStates;
                    RealMatrix expectedVdiag;
                    RealMatrix actual;
                    RealMatrix vdiags;
                    std::shared_ptr<PairedPolynomialFilter> f;
                    RealMatrix Zstar;
                    RealMatrix diff;
                    double e;
                    assert_clear();
                    testData = std::make_shared<TestData>("testPair.nc");
                    states = testData->getGroup("States");
                    matches = testData->getMatchingGroups("States_Case_");
                    assert_not_empty(matches);
                    for (int i = 0; i < matches.size(); i++) {
                        caseGroup = testData->getGroup(matches[i]);
                        order = testData->getInteger(caseGroup, "order");
                        tau = testData->getScalar(caseGroup, "tau");
                        theta = testData->getScalar(caseGroup, "theta");
                        nS = testData->getInteger(caseGroup, "nS");
                        N = testData->getInteger(caseGroup, "N");
                        times = testData->getArray(caseGroup, "times");
                        observations = testData->getArray(caseGroup, "observations");
                        expectedStates = testData->getArray(caseGroup, "expected");
                        expectedVdiag = testData->getArray(caseGroup, "vdiags");
                        f = std::make_shared<PairedPolynomialFilter>(order, tau, theta);
                        actual = ArrayXXd::Zero(N, order + 1);
                        vdiags = ArrayXXd::Zero(N, order + 1);
                        for (int j = 0; j < N; j++) {
                            Zstar = f->predict(times(j, 0));
                            e = observations(j) - Zstar(0);
                            f->update(times(j, 0), Zstar, e);
                            actual.row(j) = transpose(f->getState());
                            vdiags.row(j) = transpose(diag(f->getVRF()));
                        }
                        assert_almost_equal(actual, expectedStates);
                        assert_almost_equal(vdiags, expectedVdiag);
                    }
                    testData->close();
                    assertGreaterEqual(39.4, assert_report("Pair_test/test2CheckStates"));
                }

                void test9Coverage () {
                    std::shared_ptr<PairedPolynomialFilter> f;
                    RealMatrix Zstar;
                    f = std::make_shared<PairedPolynomialFilter>(0, 1.0, 0.5);
                    f->start(0.0, (RealVector1() << 10.).finished());
                    assertEqual(0.0, f->getTime());
                    assert_almost_equal(f->getState(), (RealVector1() << 10.).finished());
                    assertFalse(f->isFading());
                    for (int t = 1; t < 1 + 3; t++) {
                        Zstar = f->predict(t);
                        f->update(t, Zstar, 0.0);
                        assertFalse(f->isFading());
                    }
                    Zstar = f->predict(4);
                    f->update(4, Zstar, 0.0);
                    assertTrue(f->isFading());
                }

            }; // class Pair_test
        }; // namespace components
    }; // namespace polynomialfiltering

#pragma float_control(pop)

TEST_CASE("Pair_test") {
    polynomialfiltering::components::Pair_test test;

    SUBCASE("test2CheckStates") {
        test.test2CheckStates();
    }
    SUBCASE("test9Coverage") {
        test.test9Coverage();
    }
}

