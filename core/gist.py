__author__ = 'Bulatus'

from  time import time

import matlab_wrapper as mw


def extract(path):
    Ar = []
    Ar2 = []
    t1 = time()
    matlab = mw.MatlabSession()
    # print matlab.workspace.path()
    # print("raw version string from MATLAB workspace:", matlab.workspace.version())
    # matlab.eval('C:\projects\PycharmProjects\diploma\core\dem.m')
    matlab.put("mydir", path)
    print path
    matlab.eval("names = dir(mydir)")
    names = matlab.get("names")
    count = len(names)/3
    for i in range(2, count):
        curFile = names[i].name
        print curFile
        print path + curFile
        # path = "C:\projects\PycharmProjects\diploma\core\demo1.jpg"
        matlab.workspace.img1 = matlab.workspace.imread(path + curFile)
        if i == 2:
            matlab.workspace.addpath('C:\projects\PycharmProjects\diploma\core')
            # Gist Parametr estimations
            matlab.eval("clear param")
            matlab.eval("param.imageSize = [256 256];")
            matlab.eval("param.orientationsPerScale = [8 8 8 8];")
            matlab.eval("param.numberBlocks = 4;")
            matlab.eval("param.fc_prefilt = 4;")

            #Nfeatures = 512
            #Pre-allocate gist:
            #matlab.workspace.Nfeatures = matlab.eval("sum(param.orientationsPerScale)*param.numberBlocks^2;") #calculating number of feature
            t2 = time()
            #Load first image and compute gist:
            matlab.eval("[gist, param] = LMgist(img1, '', param);")  #first call
            gist1 = matlab.get("gist")
            print "Calculating gist for " + path + " - " + str(t2 - t1) + " taken"
            Ar.append(gist1)
        elif i < 0.8 * count :
            t2 = time()
            matlab.eval("[gist,param] = LMgist(img1, '', param);")
            print "Calculating gist for " + path + " - " + str(t2 - t1) + " taken"
            gist1 = matlab.get("gist")
            Ar.append(gist1)
        else:
            t2 = time()
            matlab.eval("[gist,param] = LMgist(img1, '', param);")
            print "Calculating gist for test data " + path + " - " + str(t2 - t1) + " taken"
            gist1 = matlab.get("gist")
            Ar2.append(gist1)


        # print Ar


    print len(Ar)

    return [Ar,Ar2]

if __name__ == "__main__":
    extract('C:\Sun\d\desert\\vegetation\\')
# extract('C:\Sun\d\desert\\vegetation\sun_adjkfhidmafvrhye.jpg')


