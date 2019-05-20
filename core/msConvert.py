#!/usr/python
#coding=utf-8


import os

class msConvert(object):
    '''
    init
    '''
    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile

    def __pase_command(self):
        input_command = (" wine msconvert --mzXML "
                         "/data/%s "
                         "--32 "
                         "--mz32 "
                         "--inten32 "
                         "--zlib "
                         "--outfile %s"
                         % (self.infile, self.outfile))
        return input_command

    def __docker(self, path, command = ""):
        docker_command = ("docker run --rm -e WINEDEBUG=-all %s"
                          "-v %s:/data/ msconvert"
                          % (command, path))
        return docker_command

    def run(self, path, extra=""):
        run_cmd = ("%s %s"
                   % (self.__docker(path, extra), self.__pase_command()))
        # print(run_cmd)
        return_info = os.popen(run_cmd)
        return_info= "Guomics Lab: " + '\n'.join(return_info.readlines())

        return return_info




if __name__ == "__main__":
    pass