/***** /polynomialfiltering/components/FixedMemoryFilter_test/
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
#include <polynomialfiltering/components/Fmp.hpp>
#include <polynomialfiltering/filters/PairedPolynomialFilter.hpp>
#include <polynomialfiltering/filters/FixedMemoryPolynomialFilter.hpp>
#include <TestData.hpp>




#pragma float_control(push)
#pragma float_control(precise, off)
    namespace polynomialfiltering {
        namespace components {
            
            using namespace Eigen;
            
            class FixedMemoryFilter_test {
            public:
                RealMatrix executeEstimatedState (const RealMatrix& setup, const RealMatrix& data) {
                    int order;
                    int window;
                    int M;
                    int iCheck;
                    RealMatrix times;
                    RealMatrix observations;
                    std::shared_ptr<filters::FixedMemoryFilter> fixed;
                    order = int(setup(0));
                    window = int(setup(1));
                    M = int(setup(2));
                    iCheck = int(setup(3));
                    times = data.col(0);
                    observations = data.col(1);
                    fixed = std::make_shared<filters::FixedMemoryFilter>(order, window);
                    for (int i = 0; i < M; i++) {
                        fixed->add(times(i), observations(i));
                    }
                    return fixed->transitionState(times(iCheck));
                }

                RealMatrix executeVRF (const RealMatrix& setup, const RealMatrix& data) {
                    int order;
                    int window;
                    int M;
                    int iCheck;
                    RealMatrix times;
                    RealMatrix observations;
                    std::shared_ptr<filters::FixedMemoryFilter> fixed;
                    order = int(setup(0));
                    window = int(setup(1));
                    M = int(setup(2));
                    iCheck = int(setup(3));
                    times = data.col(0);
                    observations = data.col(1);
                    fixed = std::make_shared<filters::FixedMemoryFilter>(order, window);
                    for (int i = 0; i < M; i++) {
                        fixed->add(times(i), observations(i));
                    }
                    return fixed->getVRF();
                }

                void test1CheckPerfect () {
                    std::vector<std::string> matches;
                    double tau;
                    int N;
                    Group group;
                    RealVector setup;
                    int order;
                    RealMatrix data;
                    RealMatrix actual;
                    RealMatrix expected;
                    std::shared_ptr<TestData> testData;
                    assert_clear();
                    testData = std::make_shared<TestData>("FixedMemoryFiltering.nc");
                    matches = testData->getMatchingGroups("testPerfect_");
                    assert_not_empty(matches);
                    tau = 0.1;
                    N = 25;
                    for (int i = 0; i < matches.size(); i++) {
                        group = testData->getGroup(matches[i]);
                        setup = testData->getArray(group, "setup");
                        order = int(setup(0));
                        data = testData->getArray(group, "data");
                        actual = this->executeEstimatedState(setup, data);
                        expected = testData->getArray(group, "expected");
                        assert_almost_equal(expected, actual);
                    }
                    testData->close();
                    assert_report("FixedMemoryFilter_test/test1CheckPerfect");
                }

                void test1CheckNoisy () {
                    std::vector<std::string> matches;
                    double tau;
                    int N;
                    Group group;
                    RealVector setup;
                    int order;
                    RealMatrix data;
                    RealMatrix actual;
                    RealMatrix expected;
                    std::shared_ptr<TestData> testData;
                    assert_clear();
                    testData = std::make_shared<TestData>("FixedMemoryFiltering.nc");
                    matches = testData->getMatchingGroups("testNoisy_");
                    assert_not_empty(matches);
                    tau = 0.1;
                    N = 25;
                    for (int i = 0; i < matches.size(); i++) {
                        group = testData->getGroup(matches[i]);
                        setup = testData->getArray(group, "setup");
                        order = int(setup(0));
                        data = testData->getArray(group, "data");
                        actual = this->executeEstimatedState(setup, data);
                        expected = testData->getArray(group, "expected");
                        assert_almost_equal(expected, actual);
                    }
                    testData->close();
                    assert_report("FixedMemoryFilter_test/test1CheckNoisy");
                }

                void test1CheckMidpoints () {
                    std::vector<std::string> matches;
                    double tau;
                    int N;
                    int M;
                    int window;
                    int iCheck;
                    Group group;
                    RealVector setup;
                    int offset;
                    int order;
                    RealMatrix data;
                    RealMatrix actual;
                    RealMatrix expected;
                    std::shared_ptr<TestData> testData;
                    assert_clear();
                    testData = std::make_shared<TestData>("FixedMemoryFiltering.nc");
                    matches = testData->getMatchingGroups("testMidpoints_");
                    assert_not_empty(matches);
                    tau = 0.1;
                    N = 25;
                    order = 2;
                    window = 11;
                    M = 12;
                    offset = M - window;
                    for (int i = 0; i < matches.size(); i++) {
                        group = testData->getGroup(matches[i]);
                        setup = testData->getArray(group, "setup");
                        order = int(setup(0));
                        window = int(setup(1));
                        M = int(setup(2));
                        iCheck = int(setup(3));
                        data = testData->getArray(group, "data");
                        actual = this->executeEstimatedState(setup, data);
                        expected = testData->getArray(group, "expected");
                        assert_almost_equal(expected, actual);
                    }
                    testData->close();
                    assert_report("FixedMemoryFilter_test/test1CheckMidpoints");
                }

                void test1CheckVrfs () {
                    std::vector<std::string> matches;
                    double tau;
                    int N;
                    int M;
                    int window;
                    int iCheck;
                    Group group;
                    RealVector setup;
                    int order;
                    int offset;
                    RealMatrix data;
                    RealMatrix actual;
                    RealMatrix expected;
                    std::shared_ptr<TestData> testData;
                    assert_clear();
                    testData = std::make_shared<TestData>("FixedMemoryFiltering.nc");
                    matches = testData->getMatchingGroups("testVRF_");
                    assert_not_empty(matches);
                    tau = 0.1;
                    N = 25;
                    order = 2;
                    window = 11;
                    M = 12;
                    offset = M - window;
                    for (int i = 0; i < matches.size(); i++) {
                        group = testData->getGroup(matches[i]);
                        setup = testData->getArray(group, "setup");
                        order = int(setup(0));
                        window = int(setup(1));
                        M = int(setup(2));
                        iCheck = int(setup(3));
                        data = testData->getArray(group, "data");
                        actual = this->executeVRF(setup, data);
                        expected = testData->getArray(group, "expected");
                        assert_almost_equal(expected, actual);
                    }
                    testData->close();
                    assert_report("FixedMemoryFilter_test/test1CheckVrfs");
                }

                class TestFixedMemoryFilter : public FixedMemoryFilter {
                    public:
                        TestFixedMemoryFilter (const int order) : FixedMemoryFilter(order) {
                        }

                        int getOrder () {
                            return this->order;
                        }

                        int getL () {
                            return this->L;
                        }

                }; // class TestFixedMemoryFilter 

            void test9Regresssion () {
                std::shared_ptr<TestFixedMemoryFilter> f;
                std::shared_ptr<filters::FixedMemoryFilter> fixed;
                RealMatrix Z;
                assert_clear();
                f = std::make_shared<TestFixedMemoryFilter>(4);
                assertEqual(f->getOrder(), 4);
                assertEqual(f->getL(), 51);
                fixed = std::make_shared<filters::FixedMemoryFilter>(0, 5);
                assertEqual(fixed->getTau(), 0.0);
                assertEqual(fixed->getStatus(), FilterStatus::IDLE);
                Z = ArrayXXd::Zero(1, 1);
                assert_almost_equal(Z, fixed->getVRF());
                assertEqual(fixed->getFirstVRF(), 0);
                assertEqual(fixed->getLastVRF(), 0);
                for (int i = 0; i < 5; i++) {
                    assertEqual(fixed->getN(), i);
                    fixed->add(i, i);
                    assertEqual(fixed->getStatus(), FilterStatus::INITIALIZING);
                }
                fixed->add(10, 10);
                assertEqual(fixed->getStatus(), FilterStatus::RUNNING);
                assertEqual(fixed->getTime(), 10);
                assert_almost_equal(fixed->getState(), (RealVector1() << 4.0).finished());
                assert_report("FixedMemoryFilter_test/test9Regresssion");
            }

            }; // class FixedMemoryFilter_test
        }; // namespace components
    }; // namespace polynomialfiltering

#pragma float_control(pop)

TEST_CASE("FixedMemoryFilter_test") {
    polynomialfiltering::components::FixedMemoryFilter_test test;

    SUBCASE("test1CheckPerfect") {
        test.test1CheckPerfect();
    }
    SUBCASE("test1CheckNoisy") {
        test.test1CheckNoisy();
    }
    SUBCASE("test1CheckMidpoints") {
        test.test1CheckMidpoints();
    }
    SUBCASE("test1CheckVrfs") {
        test.test1CheckVrfs();
    }
    SUBCASE("test9Regresssion") {
        test.test9Regresssion();
    }
}

