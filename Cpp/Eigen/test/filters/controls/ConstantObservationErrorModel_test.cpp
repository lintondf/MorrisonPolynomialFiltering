/***** /filters/controls/ConstantObservationErrorModel_test/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++ TEST
 */

#include <iostream>
#include <vector>
#include <cmath>
#include <netcdf.h>

#include <doctest.h>

#include <math.h>

#include <polynomialfiltering/PolynomialFilteringEigen.hpp>

#include <polynomialfiltering/filters/controls/ConstantObservationErrorModel.hpp>
#include <TestData.hpp>




#pragma float_control(push)
#pragma float_control(precise, off)
namespace filters {
    namespace controls {
        namespace ConstantObservationErrorModel_test {
            
            using namespace Eigen;
            
                void test1Scalar () {
                    /*rTS*/std::shared_ptr<TestData> testData;
                    std::vector<std::string> matches;
                    int iE;
                    RealMatrix inputCovariance;
                    RealMatrix inputInverse;
                    RealVector element;
                    double x;
                    RealMatrix Q;
                    /*rTS*/std::shared_ptr<polynomialfiltering::filters::controls::ConstantObservationErrorModel> model;
                    testData = /*eNE*/std::make_shared<TestData>;
                    matches = testData->getMatchingGroups("testScalar_");
                    for (int i = 0; i < matches.size(); i++) {
                        element = testData->getGroupVariable(matches[i], "element");
                        inputCovariance = testData->getGroupVariable(matches[i], "inputCovariance");
                        inputInverse = testData->getGroupVariable(matches[i], "inputInverse");
                        iE = int(element(0));
                        x = inputCovariance(0, 0);
                        model = /*eNE*/std::make_shared<ConstantObservationErrorModel>;
                        Q = model->getCovarianceMatrix(nullptr, 0.0, Map<RowVectorXd>( new double[1] {0.}, 1), iE);
                        assert_almost_equal(inputCovariance(0, 0), Q);
                        Q = model->getPrecisionMatrix(nullptr, 0.0, Map<RowVectorXd>( new double[1] {0.}, 1), iE);
                        assert_almost_equal(inputInverse(0, 0), Q);
                    }
                    testData->close();
                }

                void test2Matrix () {
                    /*rTS*/std::shared_ptr<TestData> testData;
                    std::vector<std::string> matches;
                    int iE;
                    RealMatrix inputCovariance;
                    RealMatrix inputInverse;
                    RealVector element;
                    RealMatrix Q;
                    /*rTS*/std::shared_ptr<polynomialfiltering::filters::controls::ConstantObservationErrorModel> model;
                    testData = TestData::make("testConstantObservationErrorModel.nc");
                    matches = testData->getMatchingGroups("testMatrix_");
                    for (int i = 0; i < matches.size(); i++) {
                        element = testData->getGroupVariable(matches[i], "element");
                        inputCovariance = testData->getGroupVariable(matches[i], "inputCovariance");
                        inputInverse = testData->getGroupVariable(matches[i], "inputInverse");
                        iE = int(element(0));
                        model = /*eNE*/std::make_shared<ConstantObservationErrorModel>;
                        Q = model->getCovarianceMatrix(nullptr, 0.0, Map<RowVectorXd>( new double[1] {0.}, 1), iE);
                        assert_almost_equal(inputCovariance(0, 0), Q);
                        Q = model->getPrecisionMatrix(nullptr, 0.0, Map<RowVectorXd>( new double[1] {0.}, 1), iE);
                        assert_almost_equal(inputInverse(0, 0), Q);
                    }
                    testData->close();
                }

                void test3MatrixMatrix () {
                    /*rTS*/std::shared_ptr<TestData> testData;
                    std::vector<std::string> matches;
                    int iE;
                    RealMatrix inputCovariance;
                    RealMatrix inputInverse;
                    RealVector element;
                    RealMatrix Q;
                    /*rTS*/std::shared_ptr<polynomialfiltering::filters::controls::ConstantObservationErrorModel> model;
                    testData = TestData::make("testConstantObservationErrorModel.nc");
                    matches = testData->getMatchingGroups("testMatrixMatrix_");
                    for (int i = 0; i < matches.size(); i++) {
                        element = testData->getGroupVariable(matches[i], "element");
                        inputCovariance = testData->getGroupVariable(matches[i], "inputCovariance");
                        inputInverse = testData->getGroupVariable(matches[i], "inputInverse");
                        iE = int(element(0));
                        model = /*eNE*/std::make_shared<ConstantObservationErrorModel>;
                        if (iE < 0) {
                            Q = model->getCovarianceMatrix(nullptr, 0.0, Map<RowVectorXd>( new double[1] {0.}, 1), iE);
                            assert_almost_equal(inputCovariance, Q);
                            Q = model->getPrecisionMatrix(nullptr, 0.0, Map<RowVectorXd>( new double[1] {0.}, 1), iE);
                            assert_almost_equal(inputInverse, Q);
                        } else {
                            Q = model->getCovarianceMatrix(nullptr, 0.0, Map<RowVectorXd>( new double[1] {0.}, 1), iE);
                            assert_almost_equal(inputCovariance(iE, iE), Q);
                            Q = model->getPrecisionMatrix(nullptr, 0.0, Map<RowVectorXd>( new double[1] {0.}, 1), iE);
                            assert_almost_equal(inputInverse(iE, iE), Q);
                        }
                    }
                    testData->close();
                }

        }; // namespace ConstantObservationErrorModel_test
    }; // namespace controls
}; // namespace filters

#pragma float_control(pop)

TEST_CASE("ConstantObservationErrorModel_test") {
    SUBCASE("test1Scalar") {
        filters::controls::ConstantObservationErrorModel_test::test1Scalar();
    }
    SUBCASE("test2Matrix") {
        filters::controls::ConstantObservationErrorModel_test::test2Matrix();
    }
    SUBCASE("test3MatrixMatrix") {
        filters::controls::ConstantObservationErrorModel_test::test3MatrixMatrix();
    }
}
