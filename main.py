__author__ = 'Bulat'

# useful libraries

import core
import  numpy as np
import core.adaboost as ada



def GISTroutine():
    paths = core.readBasePaths()

    for str in ['natural', 'indoor', 'human', 'both']:
        for i in range(0, len(paths[1][str])):
            f = paths[1][str][i]
            print "needed " + f
            path = core.getAllFiles(f)
            core.readImages(path, str)
    core.saveToBase()
  #  [X, Y , X_t, Y_t ] = core.returnBase()
  #  ada.some(X, Y, X_t, Y_t)

def ADAmodel():
     [X, Y , X_t, Y_t ] = core.returnBase()
     ada.some(X, Y, X_t, Y_t)


def main():
    """
    Main function

    """
    #.configure_custom()

    #core.cv2.waitKey()
    #core.cv2.ORB_create()
    #print help(core.cv2)
    #core.testFunc()
    #paths = core.readBasePaths()
    #print len(paths[1]['natural'])
    #print len(paths[1]['both'])
    #print len(paths[1]['human'])
    #print len(paths[1]['indoor'])
    #routine()
    ADAmodel()


if __name__ == '__main__':
    main()

