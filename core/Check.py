#!/usr/python
#coding=utf-8


import hashlib
import os

def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()



if __name__ == "__main__":
    print(GetFileMd5("../docker/openswath.20190515.tar.gz"))