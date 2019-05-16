#!/usr/python
#coding=utf-8


import os
import time

from core.Check import GetFileMd5


menu = '''

    Welcome install Guomics OpenSWATH piplines!
    
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

'''


if __name__ == "__main__":
    '''
    Install comment.
    '''
    print(menu)
    time.sleep(3)
    '''
    step 1. verify docker images.
    '''
    print("Verify docker images:")

    images_hash  = open("./core/Verify")
    openswath_image = ""
    msconvert_image = ""

    for line in images_hash:
        current = line.replace("\n","").replace("\r","").split()
        if openswath_image:
            msconvert_image = current[0]
            if GetFileMd5("./docker/" + msconvert_image) != current[1]:
                print("msconvert : Error. Please Download again and make sure it commplete.")
                exit(0)
            else:
                print("msconvert : PASS.")
        else:
            openswath_image = current[0]
            if GetFileMd5("./docker/" + openswath_image) != current[1] :
                print("OpenSWATH : Error. Please Download again and make sure it commplete.")
                exit(0)
            else:
                print("OpenSWATH : PASS.")

    '''
    step 2. install docker images.
    '''
    print("Now install images.")
    print("1.install OpenSWATH...")
    os.system("docker load --input ./docker/" + openswath_image)
    print("2.install msconvert...")
    os.system("docker load --input ./docker/" + msconvert_image)
    '''
    step 3. Test and finished.
    '''

    test_ok =  os.popen("docker run --rm openswath echo \"ok\"")
    if test_ok.read().replace("\n","").replace("\r","") != "ok":
        print("OpenSWATH Test: Fail, please reinstall later.")
        exit(0)
    else:
        print("OpenSWATH Test: Success.")
    test_ok = os.popen("docker run --rm msconvert echo \"ok\"")
    if test_ok.read().replace("\n","").replace("\r","") != "ok":
        print("msconvert Test: Fail, please reinstall later.")
        exit(0)
    else:
        print("msconvert Test: Success.")

    # finished install

    print("Finished, enjoy it(Guo Lab).")