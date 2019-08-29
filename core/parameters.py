#this file save default values used in pipeline

#there are switches to control the step processing, only when the value is "ON" the corresponding step will be runned
MSCONVERT_SWITCH = "OFF"
BULING_LIBRARY_SWITCH = "OFF"
OPENSWATH_SWITCH = "OFF"
PROPHET_SUBSAMPLE_SWITCH = "OFF"
PROPHET_MERGE_SWITCH = "OFF"
PROPHET_SCORE_SWITCH = "OFF"
STEP_5_SWITCH = "OFF"
STEP_6_SWITCH = "OFF"
STEP_7_SWITCH = "OFF"
STEP_8_SWITCH = "OFF"
STEP_9_SWITCH = "OFF"
STEP_10_SWITCH = "OFF"
STEP_11_SWITCH = "ON"
STEP_12_SWITCH = "OFF"

#there values are used to record the relative path of correspoding directory or files
# #dictionary used to save *.wiff or *.raw files
# MS_DATA = "data"
#the directory used to save *.QPQ and *.TraML
LIB_DIR = "lib"
#the directory used to save mzXML, which is the outputs of msConvert
MZXML_DIR = "mzXML"
#the directory used to save initial osw files, which are outputs of OpenSwath
OPENSWATH_OUTPUT = "output/openswath"
#the directory used to save prophet

#some default parameters values in the software invovled
#default parameters for openswath
THREADS = 8
MZ_WINDOW = 30
RT_WINDOW = 600
COMMAND = "-mz_extraction_window_unit ppm " \
      "-mz_extraction_window_ms1 20 " \
      "-mz_extraction_window_ms1_unit ppm " \
      "-use_ms1_traces " \
      "-irt_mz_extraction_window 50 " \
      "-irt_mz_extraction_window_unit ppm " \
      "-RTNormalization:estimateBestPeptides " \
      "-RTNormalization:outlierMethod none " \
      "-Scoring:stop_report_after_feature 5 " \
      "-Scoring:TransitionGroupPicker:compute_peak_quality true " \
      "-Scoring:Scores:use_ms1_mi " \
      "-Scoring:Scores:use_mi_score " \
      "-batchSize 1000 "

#default parameters for prophet
#when subsample
SUBSAMPLE_RATIO = 0.3
#when merge
MERGED_FILE_STEP_3 = "model.osw"
MERGED_FILE_STEP_7 = "model_global.osw"
#when score
LEVEL = "ms1ms2"
THREADS = 20
#where peptide or protein
CONTEXT = "global"
#use max processing methed to do step 11, this parameter value is used to specify max num cpus
NUM_OF_CPU = 10