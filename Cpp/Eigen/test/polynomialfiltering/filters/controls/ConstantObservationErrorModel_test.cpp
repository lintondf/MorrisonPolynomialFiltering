/***** /PolynomialFiltering/filters/controls/ConstantObservationErrorModel_test/
 * (C) Copyright 2019 - Blue Lightning Development, LLC.
 * D. F. Linton. support@BlueLightningDevelopment.com
 *
 * SPDX-License-Identifier: MIT
 * See separate LICENSE file for full text
 *
 * AUTO-GENERATED C++
 */

#include "polynomialfiltering/filters/controls/ConstantObservationErrorModel_test.hpp"

#pragma float_control(push)
#pragma float_control(precise, off)
namespace PolynomialFiltering {
    namespace filters {
        namespace controls {
            using namespace Eigen;
            
                void TestConstantObservationErrorModel::test1Scalar () {
                    std::shared_ptr<TestData> testData;
                    std::vector<tr> matches;
                    int iE;
                    RealMatrix inputCovariance;
                    RealMatrix inputInverse;
                    RealVector element;
                    double x;
                    RealMatrix Q;
                    std::shared_ptr<ConstantObservationErrorModel> model;
                    testData = TestData::make("testConstantObservationErrorModel.nc");
                    matches = testData.getMatchingGroups("testScalar_");
                    for (int i = 0; i < matches.size(); i++) {
                        element = testData.getGroupVariable(matches[i], "element");
                        inputCovariance = testData.getGroupVariable(matches[i], "inputCovariance");
                        inputInverse = testData.getGroupVariable(matches[i], "inputInverse");
                        iE = int(element(0));
                        x = inputCovariance(0, 0);
                        model = ConstantObservationErrorModel(x);
                        Q = model.getCovarianceMatrix(nullptr, 0.0, Map<RowVectorXd>( new double[1] {0.}, 1), iE);
                        assert_almost_equal(inputCovariance(0, 0), Q);
                        Q = model.getPrecisionMatrix(nullptr, 0.0, Map<RowVectorXd>( new double[1] {0.}, 1), iE);
                        assert_almost_equal(inputInverse(0, 0), Q);
                    }
                    testData.close;
                }

                void TestConstantObservationErrorModel::test2Matrix () {
                    std::shared_ptr<TestData> testData;
                    std::vector<tr> matches;
                    int iE;
                    RealMatrix inputCovariance;
                    RealMatrix inputInverse;
                    RealVector element;
                    double x;
                    RealMatrix Q;
                    std::shared_ptr<ConstantObservationErrorModel> model;
                    testData = TestData::make("testConstantObservationErrorModel.nc");
                    matches = testData.getMatchingGroups("testMatrix_");
                    for (int i = 0; i < matches.size(); i++) {
                        element = testData.getGroupVariable(matches[i], "element");
                        inputCovariance = testData.getGroupVariable(matches[i], "inputCovariance");
                        inputInverse = testData.getGroupVariable(matches[i], "inputInverse");
                        iE = int(element(0));
                        model = ConstantObservationErrorModel(inputCovariance(0, 0));
                        Q = model.getCovarianceMatrix(nullptr, 0.0, Map<RowVectorXd>( new double[1] {0.}, 1), iE);
                        assert_almost_equal(inputCovariance(0, 0), Q);
                        Q = model.getPrecisionMatrix(nullptr, 0.0, Map<RowVectorXd>( new double[1] {0.}, 1), iE);
                        assert_almost_equal(inputInverse(0, 0), Q);
                    }
                    testData.close;
                }

                void TestConstantObservationErrorModel::test3MatrixMatrix () {
                    std::shared_ptr<TestData> testData;
                    std::vector<tr> matches;
                    int iE;
                    RealMatrix inputCovariance;
                    RealMatrix inputInverse;
                    RealVector element;
                    double x;
                    RealMatrix Q;
                    std::shared_ptr<ConstantObservationErrorModel> model;
                    testData = TestData::make("testConstantObservationErrorModel.nc");
                    matches = testData.getMatchingGroups("testMatrixMatrix_");
                    for (int i = 0; i < matches.size(); i++) {
                        element = testData.getGroupVariable(matches[i], "element");
                        inputCovariance = testData.getGroupVariable(matches[i], "inputCovariance");
                        inputInverse = testData.getGroupVariable(matches[i], "inputInverse");
                        iE = int(element(0));
                        model = ConstantObservationErrorModel(inputCovariance, inputInverse);
                        if (iE < 0) {
                            Q = model.getCovarianceMatrix(nullptr, 0.0, Map<RowVectorXd>( new double[1] {0.}, 1), iE);
                            assert_almost_equal(inputCovariance, Q);
                            Q = model.getPrecisionMatrix(nullptr, 0.0, Map<RowVectorXd>( new double[1] {0.}, 1), iE);
                            assert_almost_equal(inputInverse, Q);
                        } else {
                            Q = model.getCovarianceMatrix(nullptr, 0.0, Map<RowVectorXd>( new double[1] {0.}, 1), iE);
                            assert_almost_equal(inputCovariance(iE, iE), Q);
                            Q = model.getPrecisionMatrix(nullptr, 0.0, Map<RowVectorXd>( new double[1] {0.}, 1), iE);
                            assert_almost_equal(inputInverse(iE, iE), Q);
                        }
                    }
                    testData.close;
                }

        }; // namespace controls
    }; // namespace filters
}; // namespace PolynomialFiltering

#pragma float_control(pop)