__author__ = 'Bulat'

# useful libraries

import core


def main():
    """
    Main function

    """
    paths = core.readBasePaths()
    f = paths[1]['natural'][1]
    path = core.getAllFiles(f)
    test_file = path
    core.siftfeature(test_file)



if __name__ == '__main__':
    main()
