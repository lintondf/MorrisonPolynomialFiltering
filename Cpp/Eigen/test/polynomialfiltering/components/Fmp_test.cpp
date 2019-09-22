/***** /polynomialfiltering/components/Fmp_test/
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
#include <TestData.hpp>




#pragma float_control(push)
#pragma float_control(precise, off)
    namespace polynomialfiltering {
        namespace components {
            
            using namespace Eigen;
            
            class Fmp_test {
            public:
                void test1CheckStates () {
                    std::shared_ptr<TestData> testData;
                    std::vector<std::string> matches;
                    int order;
                    RealMatrix setup;
                    Group states;
                    std::vector<std::string> cases;
                    std::string caseName;
                    Group caseGroup;
                    double tau;
                    double theta;
                    RealMatrix Y0;
                    RealMatrix times;
                    RealMatrix observations;
                    RealMatrix truth;
                    RealMatrix expected;
                    RealMatrix actual;
                    std::shared_ptr<RecursivePolynomialFilter> f;
                    RealMatrix Zstar;
                    double e;
                    assert_clear();
                    testData = std::make_shared<TestData>("testFMP.nc");
                    matches = testData->getMatchingGroups("States");
                    assert_not_empty(matches);
                    setup = testData->getGroupVariable(matches[0], "setup");
                    states = testData->getGroup(matches[0]);
                    cases = testData->getMatchingSubGroups(states, "Case_");
                    for (int i = 0; i < cases.size(); i++) {
                        caseName = cases[i];
                        caseGroup = testData->getSubGroup(states, caseName);
                        order = testData->getInteger(caseGroup, "order");
                        tau = testData->getScalar(caseGroup, "tau");
                        theta = testData->getScalar(caseGroup, "theta");
                        Y0 = testData->getArray(caseGroup, "Y0");
                        times = testData->getArray(caseGroup, "times");
                        observations = testData->getArray(caseGroup, "observations");
                        truth = testData->getArray(caseGroup, "truth");
                        expected = testData->getArray(caseGroup, "expected");
                        actual = ArrayXXd::Zero(times.rows(), order + 1);
                        f = Fmp::makeFmp(order, tau, theta);
                        f->start(0.0, Y0);
                        for (int j = 0; j < times.rows(); j++) {
                            Zstar = f->predict(times(j, 0));
                            e = observations(j) - Zstar(0);
                            f->update(times(j, 0), Zstar, e);
                            actual.row(j) = transpose(f->getState());
                        }
                        assert_almost_equal(actual, expected);
                    }
                    assertGreaterEqual(32.0, assert_report("Fmp_test/test1CheckStates"));
                    testData->close();
                }

                void test1CheckGammas () {
                    std::shared_ptr<TestData> testData;
                    std::vector<std::string> matches;
                    int order;
                    RealMatrix setup;
                    Group states;
                    std::vector<std::string> cases;
                    std::string caseName;
                    Group caseGroup;
                    double tau;
                    double theta;
                    RealMatrix Y0;
                    RealMatrix times;
                    RealMatrix observations;
                    RealMatrix truth;
                    RealMatrix expectedG;
                    RealMatrix actualG;
                    double nS;
                    std::shared_ptr<RecursivePolynomialFilter> f;
                    assert_clear();
                    testData = std::make_shared<TestData>("testFMP.nc");
                    matches = testData->getMatchingGroups("Gammas");
                    assert_not_empty(matches);
                    states = testData->getGroup(matches[0]);
                    cases = testData->getMatchingSubGroups(states, "Case_");
                    for (int i = 0; i < cases.size(); i++) {
                        caseName = cases[i];
                        caseGroup = testData->getSubGroup(states, caseName);
                        order = testData->getInteger(caseGroup, "order");
                        tau = testData->getScalar(caseGroup, "tau");
                        theta = testData->getScalar(caseGroup, "theta");
                        nS = testData->getScalar(caseGroup, "nS");
                        expectedG = testData->getArray(caseGroup, "G");
                        f = Fmp::makeFmp(order, tau, theta);
                        actualG = f->getCore()->getGamma(0, 1.0);
                        assert_almost_equal(nS, Emp::nSwitch(order, theta));
                        assert_almost_equal(actualG, expectedG);
                    }
                    assertGreaterEqual(0.0, assert_report("Fmp_test/test1CheckGammas"));
                    testData->close();
                }

                void test1CheckVRF () {
                    std::shared_ptr<TestData> testData;
                    std::vector<std::string> matches;
                    int order;
                    RealMatrix setup;
                    Group states;
                    std::vector<std::string> cases;
                    std::string caseName;
                    Group caseGroup;
                    double tau;
                    double theta;
                    RealMatrix Y0;
                    RealMatrix times;
                    RealMatrix observations;
                    RealMatrix truth;
                    RealMatrix expectedV;
                    RealMatrix actualV;
                    std::shared_ptr<RecursivePolynomialFilter> f;
                    assert_clear();
                    testData = std::make_shared<TestData>("testFMP.nc");
                    matches = testData->getMatchingGroups("Vrfs");
                    assert_not_empty(matches);
                    states = testData->getGroup(matches[0]);
                    cases = testData->getMatchingSubGroups(states, "Case_");
                    for (int i = 0; i < cases.size(); i++) {
                        caseName = cases[i];
                        caseGroup = testData->getSubGroup(states, caseName);
                        order = testData->getInteger(caseGroup, "order");
                        tau = testData->getScalar(caseGroup, "tau");
                        theta = testData->getScalar(caseGroup, "theta");
                        expectedV = testData->getArray(caseGroup, "V");
                        f = Fmp::makeFmp(order, tau, theta);
                        actualV = f->getCore()->getVRF(0);
                        assert_almost_equal(actualV, expectedV);
                    }
                    assertGreaterEqual(0.0, assert_report("Fmp_test/test1CheckVrfs"));
                    testData->close();
                }

                void test9CoreBasic () {
                    std::shared_ptr<ICore> core90;
                    std::shared_ptr<ICore> core95;
                    std::shared_ptr<ICore> core95half;
                    std::shared_ptr<ICore> core95double;
                    RealMatrix ad;
                    RealMatrix ah;
                    assert_clear();
                    core90 = Fmp::makeFmpCore(3, 1.0, 0.90);
                    core95 = Fmp::makeFmpCore(3, 1.0, 0.95);
                    core95half = Fmp::makeFmpCore(3, 2.0, 0.95);
                    core95double = Fmp::makeFmpCore(3, 0.5, 0.95);
                    assert_almost_equal(core90->getVRF(1), core90->getVRF(10));
                    assert_array_less(core95->getVRF(1), core90->getVRF(1));
                    ad = (arrayDivide(core95double->getVRF(1), core95->getVRF(1)));
                    ah = (arrayDivide(core95half->getVRF(1), core95->getVRF(1)));
                    assert_almost_equal(ones(3 + 1, 3 + 1), arrayTimes(ad, ah));
                    assert_almost_equal(core90->getGamma(10.0, 5.0), core90->getGamma(11.0, 5.0));
                    assert_almost_equal(core90->getGamma(10.0, 5.0), core90->getGamma(10.0, 6.0));
                    assert_almost_equal(core95->getGamma(10.0, 5.0), core95half->getGamma(10.0, 5.0));
                    assert_almost_equal(core95->getGamma(10.0, 5.0), core95double->getGamma(10.0, 5.0));
                    assert_report("Fmp_test/test9CoreBasic");
                }

                void test9Basic () {
                    int order;
                    double tau;
                    double theta;
                    RealMatrix Y0;
                    RealMatrix observations;
                    std::shared_ptr<RecursivePolynomialFilter> f;
                    double t;
                    RealMatrix Zstar;
                    double e;
                    RealMatrix actual;
                    assert_clear();
                    order = 5;
                    tau = 0.01;
                    theta = 0.9885155283985784;
                    actual = ArrayXXd::Zero(order + 1, 1);
                    Y0 = (RealVector6() <<  - 5.373000000000E+00,  - 1.125200000000E+01,  - 1.740600000000E+01,  - 1.565700000000E+01,  - 7.458400000000E+00,  - 1.467800000000E+00).finished();
                    observations = (RealVector11() <<  - 5.2565E+00,  - 2.8652E+00,  - 1.4812E+01, 4.6590E+00, 4.7380E+00,  - 7.3765E+00, 1.3271E+01, 7.3593E+00, 3.4308E+00,  - 1.1329E+00,  - 1.5789E+00).finished();
                    f = Fmp::makeFmp(order, tau, theta);
                    f->start(0.0, Y0);
                    t = 0;
                    Zstar = f->predict(t);
                    assert_almost_equal(Zstar, (RealVector6() <<  - 5.373000000000E+00,  - 1.125200000000E-01,  - 1.740600000000E-03,  - 1.565700000000E-05,  - 7.458400000000E-08,  - 1.467800000000E-10).finished());
                    e = observations(0) - Zstar(0);
                    assert_almost_equal(e, 0.11650000000000027);
                    actual = f->update(t, Zstar, e);
                    assert_almost_equal(actual, (RealVector6() << 7.800661521666E-03, 2.252446577781E-04, 3.468911273583E-06, 3.005115515478E-08, 1.388453238252E-10, 2.672957382342E-13).finished());
                    actual = f->getState();
                    assert_almost_equal(actual, (RealVector6() <<  - 5.365199338478335,  - 11.229475534222193,  - 17.37131088726417,  - 15.62694884484522,  - 7.444515467617483,  - 1.4651270426176584).finished());
                    t += 0.01;
                    Zstar = f->predict(t);
                    assert_almost_equal(Zstar, (RealVector6() <<  - 5.47836527e+00,  - 1.14039712e-01,  - 1.75279528e-03,  - 1.57014673e-05,  - 7.45916674e-08,  - 1.46512704e-10).finished());
                    e = observations(1) - Zstar(0);
                    assert_almost_equal(e, 2.6131652669594962);
                    f->update(t, Zstar, e);
                    actual = f->getState();
                    assert_almost_equal(actual, (RealVector6() <<  - 5.30339172,  - 10.89873388,  - 16.74985512,  - 15.02740172,  - 7.1477283,  - 1.405171).finished());
                    assertGreaterEqual(0.0, assert_report("Fmp_test/test9Basic"));
                }

                void test9NSwitch () {
                    std::shared_ptr<ICore> emp;
                    std::shared_ptr<ICore> fmp;
                    double tau;
                    RealMatrix taus;
                    double theta;
                    RealMatrix thetas;
                    int n;
                    int nThetas;
                    int nTaus;
                    assert_clear();
                    taus = (RealVector5() << 0.01, 0.1, 1., 10., 100.).finished();
                    nTaus = taus.size();
                    thetas = (RealVector4() << 0.90, 0.95, 0.99, 0.999).finished();
                    nThetas = thetas.size();
                    for (int order = 0; order < 5 + 1; order++) {
                        for (int itheta = 0; itheta < nThetas; itheta++) {
                            theta = thetas(itheta);
                            for (int itau = 0; itau < nTaus; itau++) {
                                tau = taus(itau);
                                emp = Emp::makeEmpCore(order, tau);
                                fmp = Fmp::makeFmpCore(order, tau, theta);
                                n = int(Emp::nSwitch(order, theta));
                            }
                        }
                    }
                }

            }; // class Fmp_test
        }; // namespace components
    }; // namespace polynomialfiltering

#pragma float_control(pop)

TEST_CASE("Fmp_test") {
    polynomialfiltering::components::Fmp_test test;

    SUBCASE("test1CheckStates") {
        test.test1CheckStates();
    }
    SUBCASE("test1CheckGammas") {
        test.test1CheckGammas();
    }
    SUBCASE("test1CheckVRF") {
        test.test1CheckVRF();
    }
    SUBCASE("test9CoreBasic") {
        test.test9CoreBasic();
    }
    SUBCASE("test9Basic") {
        test.test9Basic();
    }
    SUBCASE("test9NSwitch") {
        test.test9NSwitch();
    }
}

