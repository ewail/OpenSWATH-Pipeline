#!/usr/python
#coding=utf-8


import sys
import os
import getopt

from core import msConvert
from core import GlobaVar as gl


DEBUG = False

def comming():
    pass


menu = '''
    Welcome to Guomics msConvert piplines!

    msconvert is a command line tool for converting between various 
    file formats.Guomics Lab build it in piplines and make it easy 
    for everyone.

    msConvert:http://proteowizard.sourceforge.net/tools.shtml
    Web:http://www.guomics.com
    Date:20190516
    Team:Tiannan Guo, Hao Chen, Tiansheng Zhu .etc
    Ver:0.1

    Usage: python msconvert.py [COMMAND]

    Example: 

        python msconvert.py -i *.wiff -o /your/data
    Options:
        -i <file or Path>       specify text file containing filenames
        -o <file>       set output directory ('-' for stdout) [.]
        -c              Extra command
        
    Enjoy it!
'''

try:
    opts, args = getopt.getopt(sys.argv[1:],
                               "-h-i:-o:-c:",
                               ["help",
                                "infile=",
                                "outfile=",
                                "command"])

    for op, value in opts:
        if op in ("-h", "--help"):
            print(menu)
            sys.exit()
        elif op in ("-i", "--infile"):
            infile = value
        elif op in ("-o", "--outfile"):
            outfile = value
        elif op in ("-c", "--command"):
            command = value
        else:
            print(menu)
            sys.exit()

except getopt.GetoptError:
    print('''
    Error! Please use `python msconvert.py --help` for detail.
    Usage: python msconvert.py [COMMAND]

    Example:
    python msconvert.py -h
    python msconvert.py -i *.mzXML -o *.mzXML
    ''')
    sys.exit()

gl._init()

if DEBUG:
    gl.set_value("debug", DEBUG)

Ms = msConvert.msConvert(os.path.basename(infile), outfile)
path = os.path.dirname(infile)

return_info = Ms.run(path)
gl.set_value("msConvert_log", return_info)