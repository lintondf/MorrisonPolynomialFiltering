/***** /polynomialfiltering/filters/controls/ConstantObservationErrorModel_test/
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
#include <polynomialfiltering/components/FixedMemoryPolynomialFilter.hpp>
#include <polynomialfiltering/filters/controls/ConstantObservationErrorModel.hpp>
#include <TestData.hpp>




#pragma float_control(push)
#pragma float_control(precise, off)
    namespace polynomialfiltering {
        namespace filters {
            namespace controls {
                
                using namespace Eigen;
                
                class ConstantObservationErrorModel_test {
                public:
                    void test1Scalar () {
                        std::shared_ptr<TestData> testData;
                        std::vector<std::string> matches;
                        int iE;
                        RealMatrix inputCovariance;
                        RealMatrix inputInverse;
                        RealVector element;
                        double x;
                        RealMatrix Q;
                        std::shared_ptr<ConstantObservationErrorModel> model;
                        testData = std::make_shared<TestData>("testConstantObservationErrorModel.nc");
                        matches = testData->getMatchingGroups("testScalar_");
                        assert_not_empty(matches);
                        for (int i = 0; i < matches.size(); i++) {
                            element = testData->getGroupVariable(matches[i], "element");
                            inputCovariance = testData->getGroupVariable(matches[i], "inputCovariance");
                            inputInverse = testData->getGroupVariable(matches[i], "inputInverse");
                            iE = int(element(0));
                            x = inputCovariance(0, 0);
                            model = std::make_shared<ConstantObservationErrorModel>(x);
                            Q = model->getCovarianceMatrix(nullptr, 0.0, (RealVector1() << 0.).finished(), iE);
                            assert_almost_equal(inputCovariance(0, 0), Q);
                            Q = model->getPrecisionMatrix(nullptr, 0.0, (RealVector1() << 0.).finished(), iE);
                            assert_almost_equal(inputInverse(0, 0), Q);
                        }
                        testData->close();
                    }

                    void test2Matrix () {
                        std::shared_ptr<TestData> testData;
                        std::vector<std::string> matches;
                        int iE;
                        RealMatrix inputCovariance;
                        double ic;
                        RealMatrix inputInverse;
                        RealVector element;
                        RealMatrix Q;
                        std::shared_ptr<ConstantObservationErrorModel> model;
                        testData = std::make_shared<TestData>("testConstantObservationErrorModel.nc");
                        matches = testData->getMatchingGroups("testMatrix_");
                        assert_not_empty(matches);
                        for (int i = 0; i < matches.size(); i++) {
                            element = testData->getGroupVariable(matches[i], "element");
                            inputCovariance = testData->getGroupVariable(matches[i], "inputCovariance");
                            inputInverse = testData->getGroupVariable(matches[i], "inputInverse");
                            iE = int(element(0));
                            ic = inputCovariance(0, 0);
                            model = std::make_shared<ConstantObservationErrorModel>(ic);
                            Q = model->getCovarianceMatrix(nullptr, 0.0, (RealVector1() << 0.).finished(), iE);
                            assert_almost_equal(inputCovariance(0, 0), Q);
                            Q = model->getPrecisionMatrix(nullptr, 0.0, (RealVector1() << 0.).finished(), iE);
                            assert_almost_equal(inputInverse(0, 0), Q);
                        }
                        testData->close();
                    }

                    void test3MatrixMatrix () {
                        std::shared_ptr<TestData> testData;
                        std::vector<std::string> matches;
                        int iE;
                        RealMatrix inputCovariance;
                        RealMatrix inputInverse;
                        RealVector element;
                        RealMatrix Q;
                        std::shared_ptr<ConstantObservationErrorModel> model;
                        testData = std::make_shared<TestData>("testConstantObservationErrorModel.nc");
                        matches = testData->getMatchingGroups("testMatrixMatrix_");
                        assert_not_empty(matches);
                        for (int i = 0; i < matches.size(); i++) {
                            element = testData->getGroupVariable(matches[i], "element");
                            inputCovariance = testData->getGroupVariable(matches[i], "inputCovariance");
                            inputInverse = testData->getGroupVariable(matches[i], "inputInverse");
                            iE = int(element(0));
                            model = std::make_shared<ConstantObservationErrorModel>(inputCovariance, inputInverse);
                            if (iE < 0) {
                                Q = model->getCovarianceMatrix(nullptr, 0.0, (RealVector1() << 0.).finished(), iE);
                                assert_almost_equal(inputCovariance, Q);
                                Q = model->getPrecisionMatrix(nullptr, 0.0, (RealVector1() << 0.).finished(), iE);
                                assert_almost_equal(inputInverse, Q);
                            } else {
                                Q = model->getCovarianceMatrix(nullptr, 0.0, (RealVector1() << 0.).finished(), iE);
                                assert_almost_equal(inputCovariance(iE, iE), Q);
                                Q = model->getPrecisionMatrix(nullptr, 0.0, (RealVector1() << 0.).finished(), iE);
                                assert_almost_equal(inputInverse(iE, iE), Q);
                            }
                        }
                        testData->close();
                    }

                }; // class ConstantObservationErrorModel_test
            }; // namespace controls
        }; // namespace filters
    }; // namespace polynomialfiltering

#pragma float_control(pop)

TEST_CASE("ConstantObservationErrorModel_test") {
    polynomialfiltering::filters::controls::ConstantObservationErrorModel_test test;

    SUBCASE("test1Scalar") {
        test.test1Scalar();
    }
    SUBCASE("test2Matrix") {
        test.test2Matrix();
    }
    SUBCASE("test3MatrixMatrix") {
        test.test3MatrixMatrix();
    }
}

