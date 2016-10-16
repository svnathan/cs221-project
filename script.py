import datetime
import os
import sys
import colorama
from colorama import Fore, Back, Style

colorama.init()

totaltime = datetime.datetime.now()

time = datetime.datetime.now()
sys.argv = [os.getcwd() + '/dataset/']
execfile('parser.py')
print Fore.GREEN + 'Time to parse:\t' + str((datetime.datetime.now() - time).total_seconds()) + ' seconds' + Fore.WHITE

print Fore.GREEN + 'Total time:\t' + str((datetime.datetime.now() - totaltime).total_seconds()) + ' seconds' + Fore.WHITE
