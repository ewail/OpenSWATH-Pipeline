#!/usr/python
#coding=utf-8


import sys
import os
import getopt
import glob


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

        #gl._init()
        exec = os.path.dirname(__file__)

        print("msConvert:")
        print("msConvert: total(wiff:" + str(len(wiff)) + ";Raw:" + str(len(raw)) + ")")
        # msConvert wiff
        if len(wiff) > 0 or len(raw) > 0:
            # python msconvert.py -i *.wiff -o /your/data
            if not os.path.exists(path + "/mzXML"):
                os.makedirs(path + "/mzXML")

            for file in wiff:
                name = (os.path.basename(file)).split(".")[0] + ".mzXML"
                print("Start analysis:" + name)
                cmd = "python " + exec + "/msconvert.py -i " + file + " -o /data/mzXML/" + name
                if (os.system(cmd)) :
                    print("Status: (msconvert:wiff) failed!")
                    exit(0)
            # python msconvert.py -i *.raw -o /your/data
            for file in raw:
                name = (os.path.basename(file)).split(".")[0] + ".mzXML"
                print("Start analysis:" + name)
                cmd = "python " + exec + "/msconvert.py -i " + file + " -o /data/mzXML/" + name
                if (os.system(cmd)):
                    print("Status: (msconvert:RAW) failed!")
                    exit(0)
            print("msconvert: all file was convert completed!")

        # Build Library
        print("Build Library:")



        # Run openswath
        print("OpenSWATH:")
        get_mzXML = glob.glob(path + "/mzXML/*.mzXML")
        if len(get_mzXML) > 0:
            pass
        else:
            print("Cannot find any mzXML file! Please check your data in Path:" + path)
            exit(0)

        # Run pyprophet


        # Convert tsv file to peptides matrix


    else:
        print('''
        Your directory is NOT found! Where is your data?
        ''')

