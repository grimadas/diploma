# coding=utf-8

__author__ = 'Bulat'

# libraries
from collections import defaultdict
from os import listdir
import time
from functools import wraps
import cPickle as pickle
from PIL import Image
import gist
import xlrd
import adaboost
#THEANO Library


# const parameters given by sun database
PATH = "C:\SunAt\\" + "three_levels.xlsx"
PIC_PATH = "C:\Sun\\"
PATHS_ROW = 0
INDOOR_ROW = 1
OUTDOOR_NAT_ROW = 2
OUTDOOR_HUM_ROW = 3
BASE_PATH = "C:\\SunAT\\features.p"
#BASEFILE = "C:\SunAt\\"

def testFunc():
    pass
    #k1 = cv2.MSER_create()
    #k2 = cv2.ORB_create()
  #  k3 = cv2.ORB()
  #  k3.compute()



def retry(f):
    @wraps(f)
    def wrapped_f(*args, **kwargs):
        MAX_ATTEMPTS = 5
        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                return f(*args, **kwargs)
            except:
                print "Attempt %s/%s failed : %s", attempt, MAX_ATTEMPTS, (args, kwargs)
                time.sleep(10 * attempt)
        print "All %s attempts failed : %s", \
            MAX_ATTEMPTS, \
            (args, kwargs)

    return wrapped_f


X = []
Y = []
X_test = []
Y_test = []

#Opencv feature tracking  (depricated)
def features(paths):
    # Taken from github
   # detector_format = ["", "Grid", "Pyramid"]
    # "Dense" and "SimpleBlob" omitted because they caused the program to crash
    # "Sift" caused the program to crash

#    "FAST" – FastFeatureDetector
#    "STAR" – StarFeatureDetector
#    "SIFT" – SIFT (nonfree module)
#    "SURF" – SURF (nonfree module)
#    "ORB" – ORB
#    "BRISK" – BRISK
#    "MSER" – MSER
#    "GFTT" – GoodFeaturesToTrackDetector
#    "HARRIS" – GoodFeaturesToTrackDetector with Harris detector enabled
#    "Dense" – DenseFeatureDetector
#    "SimpleBlob" – SimpleBlobDetector

#    detector_types = ["FAST", "Dense", "SIFT", "SURF", "ORB", "MSER", "GFTT", "HARRIS"]

    #----------
    # This code was taken from opencv.org , for testing
    t1 = time.time()
    global kpAll
    global dsAll

    cur = 0
    prevtime = t1
    for path in paths:
        try:
            img = cv2.imread(path)
            k = cv2.ocl.useOpenCL()
            k2 = cv2.ORB_create()

            forb = cv2.FeatureDetector_create(detector_types[1])
            print forb
            descript = cv2.DescriptorExtractor_create(detector_types[1])
            #forb = cv2.Feature2D_create(detector_types[3])
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            sift = forb

            #sift = cv2.
            #sift = cv2.SIFT()
            # sift = cv2.FastFeatureDetector()
            #cv2

            #forb = cv2.ORB()
            kp = forb.detect(gray, None)
            kp, des = descript.compute(gray, kp)


            #  print "Kp len " + str(len(kp))
            #  print "Des len {0}", len(des)
            # print "DEs " + str(des)
            # des = sift.compute()
            # img = cv2.drawKeypoints(gray, kp) #, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            # kp, des = sift.detectAndCompute(gray, None)
            new_path = path + ".jpg"
            t2 = time.time()
            print "Writed " + path + " Time " + str(t2 - prevtime)
            prevtime = t2
            #cv2.imwrite(new_path, img)
            kpAll.append(kp)
            #desAll.append(des)
            #  print kp
            cur += 1
            del img
            # del(gray, sift, kp ) #, des)

        except MemoryError:
            print "oopes ! Memory Error"

    t3 = time.time()
    print "Done. " + "Taken time " + str(t3 - t1) + " for " + str(len(paths)) + " pict"
    print "Current length " + str(len(kpAll))


def saveToBase():
    global X
    global Y
    global X_test
    global Y_test

    pickle.dump({'X': X, "Y" : Y, 'X_test': X_test, 'Y_test': Y_test}, open(BASE_PATH, 'wb'))

def returnBase():
    global X
    global Y
    global X_test
    global Y_test
    print "Opening base file"
    t1 = time.time()
    dict = pickle.load(open(BASE_PATH, "rb"))
    t2 = time.time()
    print "Success! ", t2 - t1
    X = dict['X']
    Y = dict['Y']
    X_test = dict['X_test']
    Y_test = dict['Y_test']

    return [X,Y, X_test, Y_test]

def readImages(paths, str):
    """
     Read All images in paths
    :param paths: Paths to read all Images
    :return:
    """
    t1 = time.time()
    global X
    global Y
    global X_test
    global Y_test
    cur = 0
    prevtime = t1
    gist1, gist2 = gist.extract(paths)
    for k in gist1:
        X.append(k)
    for k in range(0, len(gist1)):
        Y.append([str])

    for k in gist2:
        X_test.append(k)

    for k in range(0, len(gist2)):
        Y_test.append([str])




    print 'Done'
    print "X len " , len(X)
    print "Y len " , len(Y)
    print "X te len " , len(X_test)
    print "Y te len " , len(Y_test)








# noinspection PyPep8Naming
def readBasePaths():
    """
        Reading xlsx file SUN database
        Get all paths with pictures
    :rtype : list with 2 element - ( 1. dictonary : direct paths - are keys, value - category
                                     2. dictonary : keys: category, value - paths)
    """
    dataset_dict = {}
    print "opening " + PATH
    dataset = xlrd.open_workbook(filename=PATH)
    print dataset
    print dataset.sheet_names()
    # we are working with 397 database
    dataset = dataset.sheet_by_name(u'SUN397')

    num_cells = dataset.nrows - 1
    curr_cell = 1
    # read all

    while curr_cell < num_cells:
        curr_cell += 1
        if dataset.cell_value(curr_cell, INDOOR_ROW) == 1.0:
            cell_value = 'indoor'
        elif dataset.cell_value(curr_cell, OUTDOOR_NAT_ROW) == 1.0:
            if dataset.cell_value(curr_cell, OUTDOOR_HUM_ROW) == 1.0:
                cell_value = 'both'
            else:
                cell_value = 'natural'
        else:
            cell_value = 'human'
        cell_path = dataset.cell_value(curr_cell, PATHS_ROW)
        dataset_dict[cell_path] = cell_value
    # Inverse dictionary
    inv_dict = defaultdict(list)
    for k, v in dataset_dict.iteritems():
        inv_dict[v].append(k)
    print "Successful extracting"

    return [dataset_dict, inv_dict]


# noinspection PyPep8Naming
def getAllFiles(path):
    """
     Gets avaliable names for using from dictonary
    :param path: The dir with of all files
    :return:
    """
    print path
    path = PIC_PATH[:-1] + path

    answer = (path + "\\").replace('/', '\\')

    print answer
    print "Ok"
    return answer












