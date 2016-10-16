import os
import sys

sys.argv = [os.getcwd() + '/dataset/']
execfile('parser.py')
