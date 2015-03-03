from sklearn.metrics import accuracy_score

__author__ = 'Bulatus'

import sklearn
from time import time

from sklearn.ensemble import AdaBoostClassifier
import matplotlib.pyplot as plt


def some(X, Y, X_test, Y_test):
    ada = AdaBoostClassifier()
    print "Train Model ---"
    t1 = time()
    ada.fit(X, Y)
    t2 = time()
    print "Model Trained ----------", t2 - t1
    test_errors = []
    cur = 1
    Y_test2 = []
    for k in Y_test:
        Y_test2.append(k[0])
    print "Testing: "
    print  Y_test2
    pred =  ada.predict(X_test)
    print pred
    accu =  1. - accuracy_score(y_true= Y_test2, y_pred= pred)
    print accu
    print "STAGED _____________"
    for test_predict in (
        ada.staged_predict(X_test)):


            test_errors.append(
            1. - accuracy_score(test_predict, Y_test2))


    print  "errorss : "
    print test_errors

