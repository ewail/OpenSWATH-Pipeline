#!/usr/python
#coding=utf-8


import sys
import os
import getopt
import glob
import multiprocessing as mp

from core import parameters


menu = '''

    Welcome to Guomics proteins piplines!

    Web:http://www.guomics.com
    Date:20190516
    Team: Hao Chen, Tiansheng Zhu, @Guomics
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

#used to parse the args input
def parse_args():
    if len(sys.argv)<2:
        print(menu)
        return False, False

    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "-h-v-p:",
                                   ["help",
                                    "version",
                                    "path"])
        if len(opts) == 0:
            print(menu)
            return False, False

        for op, value in opts:
            if op in ("-h", "--help"):
                print(menu)
                return False,False

            elif op in ("-v", "--version"):
                print("(Guomics proteins piplines)\n version : 0.1 \n Date:20190516")
                return False,False

            elif op in ("-p", "--path"):
                data_path =value
                # absolute_path = os.path.dirname(__file__)
                return True,data_path

            else:
                print(menu)
                return False,False

    except getopt.GetoptError:
        print('''
        Error! Please use `python runme.py --help` for detail.
        Usage: python runme.py [COMMAND]

        Example:
        python runme.py -h
        python runme.py -p /your/data
        ''')
        return False, None


def do_msconvert(script_path,data_path):
    path = data_path
    if os.path.exists(path):
        wiff = glob.glob(path  + "/*.wiff")
        raw = glob.glob(path + "/*.raw")

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
                mzXMLfile = os.path.join(path,parameters.MZXML_DIR,name)
                cmd = "python %s/msconvert.py -i %s -o %s"%(script_path,file,mzXMLfile)
                print(cmd)
                if (os.system(cmd)) :
                    print("Status: (msconvert:wiff) failed!")
                    exit(0)
            # python msconvert.py -i *.raw -o /your/data

            for file in raw:
                name = (os.path.basename(file)).split(".")[0] + ".mzXML"
                print("Start analysis:" + name)
                mzXMLfile = os.path.join(path,parameters.MZXML_DIR,name)
                cmd = "python %s/msconvert.py -i %s -o %s"%(script_path,file,mzXMLfile)
                # print(cmd)
                if (os.system(cmd)):
                    print("Status: (msconvert:RAW) failed!")
                    exit(0)
            print("msconvert: all file was convert completed!")
        else:
            print("no wiff or raw file is found")
    else:
        print("Your directory(%s) is NOT found! Where is your data?"%(path))


def do_buildLib():
# # # Build Library
    print("Build Library: Comming soon! Skip......")
    # output /Lib


def do_openswath(script_path,data_path):
    print("OpenSWATH:")
    path = data_path

    mzXML_folder = os.path.join(path,parameters.MZXML_DIR)
    get_mzXML = glob.glob(mzXML_folder + "/*.mzXML")

    if not os.path.exists(os.path.join(path,parameters.LIB_DIR)):
        print("Did you forget to add the Library file?(/your path/Lib/)")
        exit(0)
    # library
    lib_folder = os.path.join(path,parameters.LIB_DIR)

    get_PQP = glob.glob(lib_folder + "/*.PQP")
    #at 2019.8.22
    if len(get_PQP) != 1:
        print("too many PQP lib or no PQP lib error")
        exit(0)

    # RT library
    get_TraML = glob.glob(lib_folder + "/*.TraML")
    #at 2019.8.22
    if len(get_TraML) != 1:
        print("too many TraML lib or no TraML lib error")
        exit(0)

    #at 2019.8.22
    PQP_file = get_PQP[0]
    TraML_file = get_TraML[0]

    openswath_folder = os.path.join(path,parameters.OPENSWATH_OUTPUT)
    if len(get_mzXML) > 0:
        # openswath data
        if not os.path.exists(openswath_folder):
            os.makedirs(openswath_folder)
        # python openswath.py -i demo.mzXML -o demo.osw -tr demo.PQP -irt demo.TraML -t 8
        # python openswath.py -i demo.mzXML -o demo.osw -tr demo.PQP -irt demo.TraML -t 8 -m 30 -r 600
        for file in get_mzXML:
            name = os.path.basename(file)
            print("Start analysis:" + name)
            #2019.8.22
            osw_path = os.path.join(openswath_folder,name[:-6] + ".osw")
            cmd = "python " + script_path + "/openswath.py -i %s -o %s -p %s -t %s -s %s"%(file,osw_path,PQP_file,TraML_file,str(parameters.THREADS))
            # print(cmd)
            if (os.system(cmd)):
                print("Status: (OpenSWATH:mzXML) failed!")
                exit(0)
        print("OpenSWATH: all file was processed successfully!")
    else:
        print("Cannot find any mzXML file! Please check your data in Path:%s" + mzXML_folder)
        exit(0)

def do_prophet(script_path,data_path,mode):
    path = data_path
    openswath_folder = os.path.join(path,parameters.OPENSWATH_OUTPUT)
    subsample_ratio = parameters.SUBSAMPLE_RATIO
    merged_file_step3 = os.path.join(openswath_folder,parameters.MERGED_FILE_STEP_3)
    merged_file_step7 = os.path.join(openswath_folder, parameters.MERGED_FILE_STEP_7)

    level = parameters.LEVEL
    threads = parameters.THREADS
    context = parameters.CONTEXT
#########################################################################################################
    if mode == "subsample":
        if not os.path.exists(openswath_folder):
            print("Did you have a directory to save osws files?(%s)"%(openswath_folder))
            exit(0)

        get_osw = glob.glob(openswath_folder + "/*.osw")
        # at 2019.8.22
        if len(get_osw) == 0:
            print("have not find any osw file in %s. error!!!"%openswath_folder)
            exit(0)
        # Convert tsv file to peptides matrix

        for file in get_osw:
            name = (os.path.basename(file)).split(".")[0]
            print("Start analysis:" + name + ".osw")
            cmd = "python " + script_path + "/prophet.py subsample --out=%ss --in=%s --subsample_ratio=%s"\
                                              %(file,file,str(subsample_ratio))
            #print(cmd)
            if (os.system(cmd)):
                print("Status: (pyprophet:subsample) failed!")
                exit(0)
        print("pyprophet:%s has been done successfully!" % mode)
####################################################################################################
    elif mode.startswith("merge"):
        if mode.endswith("3"):
            merged_file = merged_file_step3
        else:
            merged_file = merged_file_step7

        if not os.path.exists(openswath_folder):
            print("Did you have a directory to save osw files?" + openswath_folder)
            exit(0)

        get_osws = glob.glob(openswath_folder + "/*.osws")
        if len(get_osws) == 0:
            print("have not find any osws file. can not merge void!!!")
            exit(0)

        lib_folder = os.path.join(path, parameters.LIB_DIR)
        get_PQP = glob.glob(lib_folder + "/*.PQP")
        # at 2019.8.22
        if len(get_PQP) != 1:
            print("too many PQP lib or no PQP lib error")
            exit(0)

        PQP_file = get_PQP[0]

        print("Start merging osws files")

        cmd = "python %s/prophet.py merge --out=%s --template=%s *.osw"%(script_path,merged_file,PQP_file)

        if mode.endswith("3"):
            cmd = cmd + "s"
        else:
            cmd = cmd + "r"
        # print(cmd)
        if (os.system(cmd)):
            print("Status: (pyprophet:merge) failed!")
            exit(0)
        print("pyprophet:%s has been done successfully!" % mode)
########################################################################################
    elif mode == "score":
        if not os.path.exists(openswath_folder):
            print("Did you have a directory to save  model.osw?(%s)"%openswath_folder)
            exit(0)

        if not os.path.exists(merged_file_step3):
            print("Can not find the %s in this directory"%parameters.MERGED_FILE_STEP_3)
            exit(0)

        print("Start giving score to %s"%parameters.MERGED_FILE_STEP_3)
        #pyprophet score --in=model.osw --level=ms1ms2 --threads 20
        cmd = "python %s/prophet.py score --in=%s --level=%s --threads %s"\
              %(script_path,merged_file_step3,level,str(threads))
        print(cmd)
        if (os.system(cmd)):
            print("Status: (pyprophet:score) failed!")
            exit(0)
        print("pyprophet:%s has been done successfully!" % mode)
########################################################################################
    elif mode == "reduce":
        if not os.path.exists(openswath_folder):
            print("Did you have a directory to save  model.osw?(%s)"%openswath_folder)
            exit(0)

        get_osw = glob.glob(openswath_folder + "/*.osw")
        if len(get_osw) == 0:
            print("have not find any osws file. can not merge void!!!")
            exit(0)

        for run in get_osw:
            name = os.path.basename(run)
            if name in [parameters.MERGED_FILE_STEP_3,parameters.MERGED_FILE_STEP_7]:
                continue

            cmd = ("python %s/prophet.py reduce --in=%s --out=%sr") %(script_path,run,run)
            # print(cmd)
            if (os.system(cmd)):
                print("Status: (pyprophet:reduce) failed!")
                exit(0)
        print("pyprophet:%s has been done successfully!" % mode)
#######################################################################################
    elif mode in ["peptide","protein"]:
        cmd = ("python %s/prophet.py %s --context=%s --in=%s") % (script_path, mode,context, merged_file_step7)
        if (os.system(cmd)):
            print("Status: (pyprophet:reduce) failed!")
            exit(0)
        print("pyprophet:%s has been done successfully!"%mode)


####################################################some steps need to define additional function#####################
def step_5(script_path,data_path):
    path = data_path

    openswath_folder = os.path.join(path,parameters.OPENSWATH_OUTPUT)
    merged_file = os.path.join(openswath_folder, parameters.MERGED_FILE_STEP_3)
    level = parameters.LEVEL
    threads = parameters.THREADS

    merged_file_3 = os.path.join(openswath_folder, parameters.MERGED_FILE_STEP_3)
    merged_file_7 = os.path.join(openswath_folder, parameters.MERGED_FILE_STEP_7)

    if not os.path.exists(openswath_folder):
        print("Did you have a directory to save osw files?(%s)" % (openswath_folder))
        exit(0)

    get_osw = glob.glob(openswath_folder + "/*.osw")
    # at 2019.8.22
    if len(get_osw) == 0:
        print("have not find any osw file in %s. error!!!" % openswath_folder)
        exit(0)

    for run in get_osw:
        if run in [merged_file_3,merged_file_7]:
            continue

        cmd = "python %s/prophet.py score --in=%s --apply_weights=%s --level=%s --threads %s"\
              %(script_path,run,merged_file,level,str(threads))
        print(cmd)
        if (os.system(cmd)):
            print("Status: (step 5) failed!")
            exit(0)
    print("step 5 has been done successfully")


def step_10(script_path,data_path):
    path = data_path
    openswath_folder = os.path.join(path, parameters.OPENSWATH_OUTPUT)
    merged_file_3 = os.path.join(openswath_folder, parameters.MERGED_FILE_STEP_3)
    merged_file_7 = os.path.join(openswath_folder, parameters.MERGED_FILE_STEP_7)
    merged_file = merged_file_7

    if not os.path.exists(openswath_folder):
        print("Did you have a directory to save osw files?(%s)" % (openswath_folder))
        exit(0)

    get_osw = glob.glob(openswath_folder + "/*.osw")
    # at 2019.8.22
    if len(get_osw) == 0:
        print("have not find any osw file in %s. error!!!" % openswath_folder)
        exit(0)

    for run in get_osw:
        if run in [merged_file_3,merged_file_7]:
            continue

        cmd = "python %s/prophet.py backpropagate --in=%s --apply_scores=%s" \
              % (script_path, run,merged_file)
        print(cmd)
        if (os.system(cmd)):
            print("Status: (step 10) failed!")
            exit(0)

    print("step 10 has been done successfully")


def step_11(script_path,data_path):

    path = data_path
    openswath_folder = os.path.join(path, parameters.OPENSWATH_OUTPUT)

    merged_file_3 = os.path.join(openswath_folder, parameters.MERGED_FILE_STEP_3)
    merged_file_7 = os.path.join(openswath_folder, parameters.MERGED_FILE_STEP_7)

    if not os.path.exists(openswath_folder):
        print("Did you have a directory to save osw files?(%s)" % (openswath_folder))
        exit(0)

    get_osw = glob.glob(openswath_folder + "/*.osw")
    # at 2019.8.22
    if len(get_osw) == 0:
        print("have not find any osw file in %s. error!!!" % openswath_folder)
        exit(0)

    pool = mp.Pool(processes=parameters.NUM_OF_CPU)  # create a process pool
    results = []
    file_list = []
    for run in get_osw:
        if run in [merged_file_3,merged_file_7]:
            continue

        cmd = "python %s/prophet.py export --in=%s" \
              % (script_path, run)
        # print(cmd)
        file_list.append(os.path.basename(run))
        results.append(pool.apply_async(os.system, (cmd,)))

    pool.close()   #close the process pool
    pool.join()   #wait for all processes in pool ends

    for num in range(len(results)):
        res = results[num]
        file = file_list[num]
        if res.get() != 0:
            print("Status:(step 11) failed when exporting %s"%file)
            exit(0)

    print("step 11 has been done successfully")

if __name__ == "__main__":
    stat,data_path = parse_args()
    if stat:
        script_path = os.path.dirname(__file__)
        print(script_path)
        if parameters.MSCONVERT_SWITCH == "ON":
            do_msconvert(script_path,data_path)
        if parameters.BULING_LIBRARY_SWITCH == "ON":
            do_buildLib()
        if parameters.OPENSWATH_SWITCH == "ON":
            do_openswath(script_path,data_path)
        if parameters.PROPHET_SUBSAMPLE_SWITCH == "ON":
            do_prophet(script_path,data_path,mode = "subsample")
        if parameters.PROPHET_MERGE_SWITCH == "ON":
            do_prophet(script_path,data_path,mode = "merge3")
        if parameters.PROPHET_SCORE_SWITCH == "ON":
            do_prophet(script_path,data_path,mode = "score")
        if parameters.STEP_5_SWITCH == "ON":
            step_5(script_path,data_path)
        if parameters.STEP_6_SWITCH == "ON":
            do_prophet(script_path,data_path, mode="reduce")
        if parameters.STEP_7_SWITCH == "ON":
            do_prophet(script_path,data_path, mode="merge7")
        if parameters.STEP_8_SWITCH == "ON":
            do_prophet(script_path,data_path, mode="peptide")
        if parameters.STEP_9_SWITCH == "ON":
            do_prophet(script_path,data_path,mode="protein")
        if parameters.STEP_10_SWITCH == "ON":
            step_10(script_path,data_path)
        if parameters.STEP_11_SWITCH == "ON":
            step_11(script_path,data_path)
        if parameters.STEP_12_SWITCH == "ON":
            pass
