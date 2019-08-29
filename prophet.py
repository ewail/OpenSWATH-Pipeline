#!/usr/python
#coding=utf-8

import sys
import os
import getopt
import glob

from core import Prophet
from core import GlobaVar as gl

DEBUG = False


menu = '''

    Welcome to Guomics Prophet piplines!

    prophet is a command line tool for estimating error rate

    corresponing to peak identification. Guomics Lab build it

    in piplines and make it easyfor everyone.

    pyPhophet :http://xxxxxx

    Web:http://www.guomics.com
    Date:20190822
    Team:Tiannan Guo, Hao Chen, Tiansheng Zhu .etc
    Ver:0.1

    Usage: python msconvert.py [COMMAND]

    Example:

        python pyprophet subsample --in=merged.osw --out=subsampled.osw --subsample_ratio=0.1

        pyprophet merge --out=model.osw --template=20190510DPHLdecoy_v6.2.PQP *.osws

        python pyprophet score --in=merged.osw --level=ms2

    Enjoy it!

'''

#declare varialbes to record the parameter values
infile = ""
level = ""
thread = 1
subsample_ratio = 1
apply = ""
context = ""
apply_score = ""

try:
    mode  = sys.argv[1]
    if mode in ["merge","score","subsample","reduce",
                "peptide","protein","backpropagate","export"]:
        opts, args = getopt.getopt(sys.argv[2:],"o:s:i:t:l:t:a:c:p:",
                                   ["out=",
                                    "subsample_ratio=",
                                    "in=",  # *.PQP
                                    "template=",  # TraML
                                    "level=",  # *.osw
                                    "threads=",
                                    "apply_weights=",
                                    "context=",
                                    "apply_scores="])
        for op, value in opts:
            if op in ("--out"):
                out = value
            elif op in ("--subsample_ratio"):
                subsample_ratio = value
            elif op in ("--in"):
                infile = value
            elif op in ("--template"):
                template = value
            elif op in ("--level"):
                level = value
            elif op in ("--threads"):
                threads = value
            elif op in ("--apply_weights"):
                apply = value
            elif op in ("--context"):
                context = value
            elif op in ("--apply_scores"):
                apply_score = value

        # merge mode has a parameter without a prefix
        if mode == "merge":
            osw_files = sys.argv[-1]
    else:
        print(menu)
        sys.exit()
except getopt.GetoptError:
    print('''
        Example:
        python pyprophet subsample --in=merged.osw --out=subsampled.osw --subsample_ratio=0.1
        pyprophet merge --out=model.osw --template=20190510DPHLdecoy_v6.2.PQP *.osws
        python pyprophet score --in=merged.osw --level=ms2
    ''')
    sys.exit()

gl._init()

if DEBUG:
    gl.set_value("debug", DEBUG)

parameterstring =""
if mode == "subsample":
    parameterstring = "--out=%s --subsample_ratio=%s --in=%s"%(out,subsample_ratio,infile)
elif mode == "merge":
    parameterstring = "--out=%s --template=%s %s"%(out,template,osw_files)
elif mode == "score":
    parameterstring = "--in=%s --level=%s --threads %s"%(infile,level,threads)
    if len(apply)>0:
        parameterstring = parameterstring + " --apply_weights=%s"%apply
elif mode == "reduce":
    parameterstring = "--in=%s --out=%sr"%(infile,infile)
elif mode == "peptide":
    parameterstring = "--context=%s --in=%s"%(context,infile)
elif mode == "protein":
    parameterstring = "--context=%s --in=%s"%(context,infile)
elif mode == "backpropagate":
    parameterstring = "--in=%s --apply_scores=%s"%(infile,apply_score)
elif mode == "export":
    parameterstring = "--in=%s"%(infile)

# print(parameterstring)
path = os.path.dirname(__file__)
pr = Prophet.Prophet(mode,parameterstring)
return_info = pr.run(path)
gl.set_value("prophet_log", return_info)