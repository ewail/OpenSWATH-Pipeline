#!/usr/python
#coding=utf-8


import sys
import os
import getopt
import glob
import os
import xml.dom.minidom
import pandas as pd



class CreateLib(object):

    '''
    init
    '''
    def __init__(self):
        pass


    def add_rt(self, pfind_fname="msmsinfo_pfind.tsv"):
        msmsinfo_pfind = pd.read_csv(pfind_fname, sep='\t')
        fnames = msmsinfo_pfind["mzXML.file"].unique()
        msmsinfo = pd.DataFrame()
        for f in fnames:
            print("Adding RT to " + f)
            rt = []
            scan_index = 0
            dom = xml.dom.minidom.parse(f + ".mzXML")
            root = dom.documentElement
            itemlist = root.getElementsByTagName('scan')
            msmsinfo_pfind_f = msmsinfo_pfind[msmsinfo_pfind['mzXML.file'] == f]
            n = msmsinfo_pfind_f.shape[0]
            length = len(itemlist)
            for i in range(0, n):
                while (int(itemlist[scan_index].getAttribute("num")) != msmsinfo_pfind_f.iloc[i, 1] and (
                        length - 1) > scan_index):
                    scan_index = scan_index + 1

                raw_rt = itemlist[scan_index].getAttribute("retentionTime")
                raw_rt = raw_rt[2:]
                raw_rt = raw_rt[:-1]
                rt.append(raw_rt)
                # scan_index = scan_index + 1
            msmsinfo_pfind_f.insert(6, "RetentionTime", rt)
            msmsinfo = msmsinfo.append(msmsinfo_pfind_f)

        msmsinfo.to_csv(os.path.dirname(pfind_fname) + "/msmsinfo.tsv", sep='\t', index=False)


