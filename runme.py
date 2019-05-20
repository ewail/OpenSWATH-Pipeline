#!/usr/python
#coding=utf-8


import sys
import os
import getopt
import glob


from core import GlobaVar as gl

menu = '''

    Welcome to Guomics proteins piplines!

    Web:http://www.guomics.com
    Date:20190516
    Team:Tiannan Guo, Hao Chen, Tiansheng Zhu .etc
    Ver:0.1

    Usage: python runme.py [COMMAND]

    Example: 

        python runme.py -p /your/path
    Options:
        -p <Path>       specify data file in this directory.
        -h              display this information.
        -v              version.

    Enjoy it!
'''

path = ""

try:

    opts, args = getopt.getopt(sys.argv[1:],
                               "-h-v-p:",
                               ["help",
                                "version",
                                "path"])

    for op, value in opts:
        if op in ("-h", "--help"):
            print(menu)
            sys.exit()
        elif op in ("-v", "--version"):
            print("(Guomics proteins piplines)\n version : 0.1 \n Date:20190516")
            sys.exit()
        elif op in ("-p", "--path"):
            path = value
        else:
            print(menu)
            sys.exit()
except getopt.GetoptError:
    print('''
    Error! Please use `python runme.py --help` for detail.
    Usage: python runme.py [COMMAND]

    Example:
    python runme.py -h
    python runme.py -p /your/data
    ''')
    sys.exit()

# check your data path
if not path:
    print('''
        Error! Please use `python runme.py --help` for detail.
        Usage: python runme.py [COMMAND]

        Example:
        python runme.py -h
        python runme.py -p /your/data
        ''')
    sys.exit()
else:
    if os.path.exists(path):
        wiff = glob.glob(path + "/*.wiff")
        raw = glob.glob(path + "/*.raw")

        gl._init()
        exec = os.path.dirname(__file__)

        # msconvert wiff
        if len(wiff) > 0 :
            gl.set_value("path", path)
            # python msconvert.py -i *.wiff -o /your/data
            if not os.path.exists(path + "/mzXML"):
                os.makedirs(path + "/mzXML")
            cmd = "python " + exec + "/msconvert.py -i " + path + "/*.wiff -o " + path + "/mzXML"
            if (not os.system(cmd)) :
                print("Status: (msconvert) failed!")
                exit(0)

        # msconvert raw
        if len(raw) > 0 :
            gl.set_value("path", path)
            # python msconvert.py -i *.raw -o /your/data
            if not os.path.exists(path + "/mzXML"):
                os.makedirs(path + "/mzXML")
            cmd = "python " + exec + "/msconvert.py -i " + path + "/*.raw -o " + path + "/mzXML"
            if (not os.system(cmd)):
                print("Status: (msconvert) failed!")
                exit(0)


        # openswath


        # run openswath


    else:
        print('''
        Your directory is NOT found! Where is your data?
        ''')

