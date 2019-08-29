#!/usr/python
#coding=utf-8

import os
import getopt

from core import GlobaVar as gl

#at 2019.8.23

class Prophet(object):
    '''
    init
    '''
    def __init__(self, mode, parameter_string):
        self.mode = mode
        self.apply = ""
        paras = str.split(parameter_string)
        opts, args = getopt.getopt(paras,"o:s:i:t:l:t:a:c:p:",
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
                self.out = value
            elif op in ("--subsample_ratio"):
                self.subsample_ratio = value
            elif op in ("--in"):
                self.infile = value
            elif op in ("--template"):
                self.template = value
            elif op in ("--level"):
                self.level = value
            elif op in ("--threads"):
                self.threads = value
            elif op in ("--apply_weights"):
                self.apply = value
            elif op in ("--context"):
                self.context = value
            elif op in ("--apply_scores"):
                self.apply_score = value
        #merge mode has a parameter without a prefix
        if mode == "merge":
            self.osw_files = args[0]


    def __pase_command(self):
        input_command = ""
        if self.mode == "subsample":
            input_command = ("pyprophet subsample"
                             " --out=%s"
                             " --subsample_ratio=%s"
                             " --in=%s"
                             )%(self.out,self.subsample_ratio,self.infile)
        elif self.mode == "merge":
            input_command = ("pyprophet merge"
                             " --out=%s"
                             " --template=%s"
                             " %s"
                             )%(self.out,self.template,self.osw_files)
        elif self.mode == "score": # in score mode
            input_command = ("pyprophet score"
                             " --in=%s"
                             " --level=%s"
                             " --threads %s"
                             )%(self.infile,self.level,self.threads)
            if len(self.apply)>0:
                input_command = input_command + " --apply_weights=%s"%self.apply

        elif self.mode == "reduce":
            input_command = ("pyprophet reduce"
                             " --in=%s"
                             " --out=%sr"
                             )%(self.infile, self.infile)
        elif self.mode == "peptide":
            input_command = ("pyprophet peptide"
                             " --context=%s"
                             " --in=%s"
                             )% (self.context, self.infile)
        elif self.mode == "protein":
            input_command = ("pyprophet protein"
                              " --context=%s"
                             " --in=%s"
                             )% (self.context, self.infile)
        elif self.mode == "backpropagate":
            input_command = ("pyprophet backpropagate"
                             " --in=%sr"
                             " --apply_scores=%s"
                             )% (self.infile, self.apply_score)
        elif self.mode == "export":
            input_command = ("pyprophet export"
                             " --in=%s"
                             )% (self.infile)


        return input_command

    def __docker(self, path, command = ""):
        docker_command = ("docker run --rm %s"
                          "-v %s:/data/ openswath"
                          % (command, path))
        return docker_command

    def run(self, path, extra=""):
        run_cmd = ("%s %s"
                   % (self.__docker(path, extra), self.__pase_command()))
        print(run_cmd)
        if gl.get_value("debug"):
            print(run_cmd)
            return_info = "DEBUG: " + run_cmd
            return return_info
        else:
            return_info = os.popen(run_cmd)
            return_info= "Guomics Lab: " + '\n'.join(return_info.readlines())

            return return_info




if __name__ == "__main__":
    pass