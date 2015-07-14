#-*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

# docker内部でタスクを行うmainスクリプト
import wrapper_mecab
import wrapper_termextract
import data_connector
import ConfigParser
import os
import sys
import logging
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

"""
1 data receiverで標準入力を受け取る
2 jsonで保存する
3 term extractorを呼び出す。辞書に保存する
4 mecabを呼び出す
5 標準出力でjson出力する
"""
#mode = "debug"
mode = "main"

abs_path = os.path.abspath(sys.argv[0])
abs_path_dir = os.path.dirname(abs_path)
sys.path.append(abs_path_dir)
os.chdir(abs_path_dir)

pathInitialFile = "../settings/dockerProcess.ini"

ini = ConfigParser.SafeConfigParser()
if os.path.exists(pathInitialFile):
    ini.read(pathInitialFile)
    logging.debug("Initialize setting file from {}".format(pathInitialFile))
else:
    sys.stderr.write("%s Not Found" % pathInitialFile)
    sys.exit(2)

temporaryJsonPath = os.path.join(ini.get("FilePath", "resourceDir"), ini.get("FileName", "receivedDataPath"))
resourceDir = ini.get("FilePath", "resourceDir")
pathPerlScriptDir = ini.get("FilePath", "pathPerlScriptDir")
pathNeologdDict = ini.get("FilePath", "neologdDictPath")

threshold = float(ini.get("Params", "threshold"))
osType = ini.get("Params", "osType")

if mode=="main":
    # read json document from StdIn
    inputDocument = data_connector.StdIn()
    # save input document in temporary
    data_connector.SaveTemporary(pythoned_json=inputDocument, path_temporary_save=temporaryJsonPath)
    logging.debug("received data is saved at: {}".format(temporaryJsonPath))


# calculate multi complex nouns probability and set them as new words
pathSaveMecabDict = wrapper_termextract.main(pathJsonDocument=temporaryJsonPath, resourceDir=resourceDir,
                                             pathPerlDir=pathPerlScriptDir, threshold=threshold)
logging.debug("Term Extract process is finished correctly")

pathUserDictCsv = os.path.join(resourceDir, ini.get("FileName", "termDictPath"))
documentPath = os.path.join(resourceDir, ini.get("FileName", "receivedDataPath"))
pathAnalyzedData = os.path.join(resourceDir, ini.get("FileName", "analyzedDataPath"))

# split into tokens by MeCab with generated dictionary
pathAnalyzedData = wrapper_mecab.MecabWrapperMain(pathUserDictCsv, documentPath, pathAnalyzedData, osType, pathNeologdDict)
logging.debug("analyzed result is saved at: {}".format(pathAnalyzedData))

# stdOut analyzed result
analyzedDocument = data_connector.MergeAnalyzedData(documentPath, pathAnalyzedData)
data_connector.StdOut(analyzedDocument)

if mode=="main":
    os.remove(documentPath)
    os.remove(pathAnalyzedData)


