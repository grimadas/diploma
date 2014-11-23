__author__ = 'Bulat'

# libraries
from collections import defaultdict

import xlrd
from os import listdir
import cv2
import time
from functools import wraps
import numpy as np


# const parameters given by sun database
PATH = "C:\SunAt\\" + "three_levels.xlsx"
PIC_PATH = "C:\Sun\\"
PATHS_ROW = 0
INDOOR_ROW = 1
OUTDOOR_NAT_ROW = 2
OUTDOOR_HUM_ROW = 3


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


def siftfeature(paths):

    #Taken from github
    detector_format = ["","Grid","Pyramid"]
    # "Dense" and "SimpleBlob" omitted because they caused the program to crash
    detector_types = ["FAST","STAR","SIFT","SURF","ORB","MSER","GFTT","HARRIS"]

    #----------
    # This code was taken from opencv.org , for testing
    t1 = time.time()
    kpAll = []
    desAll = []
    cur = 0
    prevtime = t1
    for path in paths:
        try:
            img = cv2.imread(path)
            #forb = cv2.FeatureDetector_create(detector_types[1])
            #descript = cv2.DescriptorExtractor_create(detector_types[1])
            forb = cv2.Feature2D_create(detector_types[1])
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            sift = forb
            #sift = cv2.StarDetector()
            #sift = cv2.SIFT()
           # sift = cv2.FastFeatureDetector()
            #cv2

            forb = cv2.SIFT()
            kp = forb.detect(gray, None)
            kp,des = forb.compute(gray, kp)
            #print kp
           # print "DEs " + str(des)
           # des = sift.compute()
          #  img = cv2.drawKeypoints(gray, kp, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
           # kp, des = sift.detectAndCompute(gray, None)
            new_path = path[:-4] + "_sift.jpg"
            t2 = time.time()
            print "Writed " + new_path + " Time " + str(t2 - prevtime)
            prevtime = t2
            # cv2.imwrite(new_path, img)
            kpAll.append(kp)
            #desAll.append(des)
          #  print kp
            cur +=1
            del img
           # del(gray, sift, kp ) #, des)

        except MemoryError:
           print "oopes"

    t3 = time.time()
    print "Done " + "Taken time " + str(t3 - t1) + " for " + str(len(paths)) + " pict"


# noinspection PyPep8Naming
def readBasePaths():
    """
        Reading xlsx file SUN database
        Get all paths with pictures
    :rtype : list with 2 element - ( dictonaries : direct paths - are keys and inverse
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

    :param path: The dir with of all files
    :return:
    """
    print path
    path = PIC_PATH[:-1] + path
    files_path = listdir(path)
    answer = [(path + '\\' + x).replace('/', '\\') for x in files_path]
    del files_path
    print "Ok"
    return answer












