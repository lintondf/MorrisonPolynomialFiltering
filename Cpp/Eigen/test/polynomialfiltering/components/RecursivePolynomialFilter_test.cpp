/***** /polynomialfiltering/components/RecursivePolynomialFilter_test/
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
#include <TestData.hpp>




#pragma float_control(push)
#pragma float_control(precise, off)
    namespace polynomialfiltering {
        namespace components {
            
            using namespace Eigen;
            
            class RecursivePolynomialFilter_test {
            public:
                class PurePredictCore : public ICore {
                    public:
                        PurePredictCore (const int order) {
                            this->order = order;
                        }

                        int getSamplesToStart () {
                            return 1;
                        }

                        RealVector getGamma (const double t, const double dtau) {
                            RealVector g;
                            g = ArrayXd::Zero(this->order + 1);
                            return g;
                        }

                        RealMatrix getVRF (const int n) {
                            RealMatrix Z;
                            Z = ArrayXXd::Zero(this->order + 1, this->order + 1);
                            return Z;
                        }

                        double getFirstVRF (const int n) {
                            return 0.0;
                        }

                        double getLastVRF (const int n) {
                            return 0.0;
                        }

                    protected:
                        int order;
                }; // class PurePredictCore 

            class PureObservationCore : public ICore {
                public:
                    PureObservationCore (const int order) {
                        this->order = order;
                    }

                    int getSamplesToStart () {
                        return 2;
                    }

                    RealVector getGamma (const double t, const double dtau) {
                        RealVector g;
                        g = 1.0 + ArrayXd::Zero(this->order + 1);
                        return g;
                    }

                    RealMatrix getVRF (const int n) {
                        RealMatrix Z;
                        Z = ArrayXXd::Zero(this->order + 1, this->order + 1);
                        return Z;
                    }

                    double getFirstVRF (const int n) {
                        return 0.0;
                    }

                    double getLastVRF (const int n) {
                        return 0.0;
                    }

                protected:
                    int order;
            }; // class PureObservationCore 

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
            std::shared_ptr<ICore> core;
            std::shared_ptr<RecursivePolynomialFilter> f;
            RealVector Zstar;
            double e;
            RealMatrix V;
            assert_clear();
            testData = std::make_shared<TestData>("testRecursivePolynomialFilter.nc");
            matches = testData->getMatchingGroups("testPurePredict_");
            assert_not_empty(matches);
            for (int iMatch = 0; iMatch < matches.size(); iMatch++) {
                setup = testData->getGroupVariable(matches[iMatch], "setup");
                times = testData->getGroupVariable(matches[iMatch], "times");
                truth = testData->getGroupVariable(matches[iMatch], "truth");
                observations = testData->getGroupVariable(matches[iMatch], "observations");
                N = int(setup(0));
                order = int(setup(1));
                tau = setup(2);
                actual = ArrayXXd::Zero(N, order + 1);
                actual.row(0) = truth.row(0);
                core = std::make_shared<PurePredictCore>(order);
                f = std::make_shared<RecursivePolynomialFilter>(order, tau, core);
                f->start(times(0), truth.row(0));
                for (int i = 1; i < N; i++) {
                    Zstar = f->predict(times(i));
                    e = observations(i) - Zstar(0);
                    f->update(times(i), Zstar, e);
                    actual.row(i) = transpose(f->getState());
                    V = f->getVRF();
                    assert_almost_equal(V, zeros(order + 1, order + 1));
                }
                expected = testData->getGroupVariable(matches[iMatch], "expected");
                assert_almost_equal(actual, expected);
            }
            assertGreaterEqual(0.0, assert_report("RecursivePolynomialFilter_test/test1PurePredict"));
            testData->close();
        }

        void test1PureObservation () {
            std::shared_ptr<TestData> testData;
            std::vector<std::string> matches;
            int N;
            int order;
            double tau;
            RealMatrix setup;
            RealMatrix times;
            RealMatrix truth;
            RealMatrix observations;
            RealMatrix es;
            RealMatrix Zstars;
            RealMatrix innovation;
            RealMatrix innovations;
            RealMatrix actual;
            RealMatrix expected;
            std::shared_ptr<ICore> core;
            std::shared_ptr<RecursivePolynomialFilter> f;
            RealVector Zstar;
            double e;
            RealMatrix V;
            assert_clear();
            testData = std::make_shared<TestData>("testRecursivePolynomialFilter.nc");
            matches = testData->getMatchingGroups("testPureObservation_");
            assert_not_empty(matches);
            for (int iMatch = 0; iMatch < matches.size(); iMatch++) {
                setup = testData->getGroupVariable(matches[iMatch], "setup");
                times = testData->getGroupVariable(matches[iMatch], "times");
                truth = testData->getGroupVariable(matches[iMatch], "truth");
                observations = testData->getGroupVariable(matches[iMatch], "observations");
                N = int(setup(0));
                order = int(setup(1));
                tau = setup(2);
                es = testData->getGroupVariable(matches[iMatch], "es");
                Zstars = testData->getGroupVariable(matches[iMatch], "Zstars");
                innovations = testData->getGroupVariable(matches[iMatch], "innovations");
                expected = testData->getGroupVariable(matches[iMatch], "expected");
                actual = ArrayXXd::Zero(N, order + 1);
                actual.row(0) = truth.row(0);
                core = std::make_shared<PureObservationCore>(order);
                f = std::make_shared<RecursivePolynomialFilter>(order, tau, core);
                f->start(times(0), truth.row(0));
                for (int i = 1; i < N; i++) {
                    Zstar = f->predict(times(i));
                    assert_almost_equal(Zstar, transpose(Zstars.row(i)));
                    e = observations(i) - Zstar(0);
                    assert_almost_equal(e, es(i));
                    innovation = f->update(times(i), Zstar, e);
                    assert_almost_equal(innovation, transpose(innovations.row(i)));
                    actual.row(i) = transpose(f->getState());
                    V = f->getVRF();
                    assert_almost_equal(V, zeros(order + 1, order + 1));
                }
                assert_almost_equal(actual, expected);
            }
            assertGreaterEqual(22.0, assert_report("RecursivePolynomialFilter_test/test1PureObservation"));
            testData->close();
        }

        void test9Coverage () {
            std::shared_ptr<ICore> core;
            std::shared_ptr<RecursivePolynomialFilter> f;
            std::shared_ptr<RecursivePolynomialFilter> g;
            std::string name;
            RealVector Zstar;
            RealMatrix I;
            assert_clear();
            core = std::make_shared<PureObservationCore>(2);
            f = std::make_shared<RecursivePolynomialFilter>(2, 1.0, core);
            assertEqual(2, f->getOrder());
            assertEqual(1.0, f->getTau());
            f->setName("hello");
            name = f->getName();
            assertEqual(f->getStatus(), FilterStatus::IDLE);
            f->start(0.0, (RealVector3() << 1.0, 2.0, 3.0).finished());
            assertEqual(f->getStatus(), FilterStatus::IDLE);
            assertEqual(f->getFirstVRF(), 0.0);
            assertEqual(f->getLastVRF(), 0.0);
            Zstar = f->predict(1.0);
            f->update(1.0, Zstar, 0.0);
            assertEqual(f->getStatus(), FilterStatus::INITIALIZING);
            Zstar = f->predict(2.0);
            f->update(2.0, Zstar, 0.0);
            assertEqual(f->getStatus(), FilterStatus::RUNNING);
            assert_almost_equal(f->getState(), (RealVector3() << 11.0, 8.0, 3.0).finished());
            assert_almost_equal(f->transitionState(4.0), (RealVector3() << 33.0, 14.0, 3.0).finished());
            assertEqual(2, f->getN());
            assertEqual(RecursivePolynomialFilter::effectiveTheta(2, 0), 0);
            assert_almost_equal(RecursivePolynomialFilter::effectiveTheta(2, 10), 0.56673);
            g = std::make_shared<RecursivePolynomialFilter>(2, 1.0, core);
            g->copyState(f);
            assert_almost_equal(g->getState(), (RealVector3() << 11.0, 8.0, 3.0).finished());
            assert_report("RecursivePolynomialFilter_test/test9Coverage");
        }

            }; // class RecursivePolynomialFilter_test
        }; // namespace components
    }; // namespace polynomialfiltering

#pragma float_control(pop)

TEST_CASE("RecursivePolynomialFilter_test") {
    polynomialfiltering::components::RecursivePolynomialFilter_test test;

    SUBCASE("test1PurePredict") {
        test.test1PurePredict();
    }
    SUBCASE("test1PureObservation") {
        test.test1PureObservation();
    }
    SUBCASE("test9Coverage") {
        test.test9Coverage();
    }
}

