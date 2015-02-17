__author__ = 'Bulat'

# useful libraries

import core

import pylearn2 as P

from pylearn2 import rbm_tools as t1

def routine():
    paths = core.readBasePaths()
    print paths[1]['natural']
    for i in range(0, 10):
        f = paths[1]['natural'][i]
        path = core.getAllFiles(f)
        test_file = path
        core.readImages(test_file)

def main():
    """
    Main function

    """
   # P.configure_custom()

    #core.cv2.waitKey()
   # core.cv2.ORB_create()
   # print help(core.cv2)
  #
  #   core.testFunc()
    routine()

if __name__ == '__main__':
    main()
