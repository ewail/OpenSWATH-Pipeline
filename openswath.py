#!/usr/python
#coding=utf-8


import sys
import getopt

from core import OpenSWATH
from core import GlobaVar as gl

def comming():
    pass

menu ='''

    Welcome to Guomics OpenSWATH piplines!
    
    The OpenSWATH Workflow enables targeted data analysis of 
    data-independent acquisition (DIA) or SWATH-MS proteomic data. 
    The main workflow consists of OpenSWATH, PyProphet, TRIC, IPF 
    and TAPIR. This website provides documentation on installation 
    and application of the tools.
    
    Guomics Lab build it in piplines and make it easy for everyone.
    
    Web:http://www.guomics.com
    Date:20190516
    Team:Tiannan Guo, Hao Chen, Tiansheng Zhu .etc
    Ver:0.1
    
    Usage: python openswath.py [COMMAND]
    
    Example: 
    
        python openswath.py -i demo.mzXML -o demo.osw -t 8
    Options:
        -i <files>*     Input files separated by blank (valid formats: 'mzML', 'mzXML', 'sqMass')
        -tr <file>*     Transition file ('TraML','tsv','pqp') (valid formats: 'traML', 'tsv', 'pqp')
        -irt <file>     Transition file ('TraML') (valid formats: 'traML', 'tsv', 'pqp')
        -o <file>       OSW output file (PyProphet-compatible SQLite file) (valid formats: 'osw')
        -t <n>          Sets the number of threads allowed to be used by the TOPP tool (default: '1')
        -m <double>     Extraction window in Thomson or ppm (see mz_extraction_window_unit) (default: '0.05' min: '0.0')
        -r <double>     Only extract RT around this value (-1 means extract over the whole range, a value of 600 means to extract around +/- 300 s of the expected elution). (default: '600.0')
        -c              Extra command
    
    Enjoy it!
'''

try:

    opts, args = getopt.getopt(sys.argv[1:],
                               "-h-i:-tr:-irt:-o:-t:-m:-r:-c:",
                               ["help",
                                "infile=",
                                "tr_file=",
                                "tr_irt=",
                                "out_osw=",
                                "threads=",
                                "mz_extraction_window",
                                "rt_extraction_window",
                                "command"])

    for op, value in opts:
        if op in("-h","--help"):
            print(menu)
            sys.exit()
        elif op in ("-i", "--infile"):
            infile = value
        elif op in ("-o", "--out_osw"):
            out_osw = value
        elif op in ("-tr", "--tr_file"):
            tr_file = value
        elif op in ("-irt", "--tr_irt"):
            tr_irt = value
        elif op in ("-t", "--threads"):
            threads = value
        elif op in ("-m", "--mz_extraction_window"):
            mz_extraction_window = value
        elif op in ("-r", "--rt_extraction_window"):
            rt_extraction_window = value
        elif op in ("-c", "--command"):
            command = value
        else:
            print(menu)
            sys.exit()
except getopt.GetoptError:
    print('''
    Error! Please use `python openswath.py --help` for detail.
    Usage: python openswath.py [COMMAND]
    
    Example:
    python openswath.py -h
    python openswath.py -i *.mzXML -o *.osw -t 8
    ''')
    sys.exit()

Op = OpenSWATH.OpenSWATH(infile,
               tr_file,
               tr_irt,
               out_osw,
               threads,
               mz_extraction_window,
               rt_extraction_window,
               command)

path = gl.get_value('path')
return_info = Op.run(path)

gl.set_value("Openswath_log", return_info)