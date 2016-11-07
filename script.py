import os
import sys
import datetime
import colorama
from colorama import Fore, Back, Style

colorama.init()

totaltime = datetime.datetime.now()

time = datetime.datetime.now()
sys.argv = [os.getcwd()]
execfile('test.py')
print Fore.GREEN + 'Time to run test.py:\t\t' + str((datetime.datetime.now() - time).total_seconds()) + ' seconds' + Fore.WHITE

time = datetime.datetime.now()
sys.argv = [os.getcwd()]
execfile('nlp_algos.py')
print Fore.GREEN + 'Time to run nlp_algos.py:\t' + str((datetime.datetime.now() - time).total_seconds()) + ' seconds' + Fore.WHITE

print Fore.GREEN + 'Total time:\t\t\t' + str((datetime.datetime.now() - totaltime).total_seconds()) + ' seconds' + Fore.WHITE