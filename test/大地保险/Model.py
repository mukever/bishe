# -*- coding:utf-8 -*-

import time
class Model:

    def getmodel(self,train_x,train_y,root,test_data,test_y = []):
        model_save = {}
        class_ifiers = Classifier()
        test_classifiers = ['NB', 'KNN', 'LR', 'RF', 'DT', 'SVM', 'GBDT']
        classifiers = {'NB': class_ifiers.naive_bayes_classifier,
                       'KNN': class_ifiers.knn_classifier,
                       'LR': class_ifiers.logistic_regression_classifier,
                       'RF': class_ifiers.random_forest_classifier,
                       'DT': class_ifiers.decision_tree_classifier,
                       'SVM': class_ifiers.svm_classifier,
                       'SVMCV': class_ifiers.svm_cross_validation,
                       'GBDT': class_ifiers.gradient_boosting_classifier
                       }
        for classifier in test_classifiers:
            print '******************* %s ********************' % classifier
            start_time = time.time()
            model = classifiers[classifier](train_x, train_y)
            print 'training took %fs!' % (time.time() - start_time)
            # if model_save_file != None:
            model_save[classifier] = model
        # for p in os.listdir(root):
        #     start_time = time.time()
        #     test = Beijing(4)
        #     test_data = []
        #     test_x, test_y = test.dofile(root, p)
        #     data_ = list(test_x)
        #     for i in xrange(len(data_)):
        #         test_data.append(data_[i])

            # print "Test",test_y
        start_time_1 = time.time()
        time1 = start_time_1 - start_time
        for classifier in test_classifiers:
            start_time = time.time()
            # print test_x
            predict = model_save[classifier].predict(test_data)

            time2 = time.time() - start_time

            # print "Pred", predict
            print classifier, "图片计算总时间", time1 + time2
            # accuracy = metrics.accuracy_score(test_y, predict)
            # print 'accuracy: %.2f%%' % (100 * accuracy)
            error = 0
            for i in xrange(len(predict)/4):
                # print "test:",test_y[i*4+0],test_y[i*4+1],test_y[i*4+2],test_y[i*4+3],
                # print 'pred:',predict[i*4+0],predict[i*4+1],predict[i*4+2],predict[i*4+3]

                if test_y[i*4+0] != predict[i*4+0] or test_y[i*4+1] != predict[i*4+1] or test_y[i*4+2] != predict[i*4+2] or test_y[i*4+3] != predict[i*4+3]:
                    error +=1
                    print "test:", test_y[i * 4 + 0], test_y[i * 4 + 1], test_y[i * 4 + 2], test_y[i * 4 + 3],
                    print 'pred:',predict[i*4+0],predict[i*4+1],predict[i*4+2],predict[i*4+3]

            total = len(predict)/4
            print total
            print error
            print 'accuracy: %.2f%%' % (100 * (total-error)*1.0/total)