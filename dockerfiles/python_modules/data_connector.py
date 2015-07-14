#-*- coding: utf-8 -*-
__author__ = 'kensuke-mi'
import sys
import json
import codecs
import os
import io_operator

# コンテナ外部から１日分の投稿分JSONを標準入力で受け取るコネクタ
# 受け取ったJSONは/analysis_data/received.jsonに保存
# received.jsonは処理が終わったら削除


def StdIn():
    pythoned_json = json.load(sys.stdin, encoding='utf-8')

    return pythoned_json


def SaveTemporary(pythoned_json, path_temporary_save = '/analysis_data/received.json'):

    str_json = json.dumps(obj=pythoned_json, ensure_ascii=False, indent=4, encoding='utf-8')
    with codecs.open(filename=path_temporary_save, mode='w', encoding='utf-8') as f:
        f.write(str_json)


def StdOut(processed_obj):
    str_json = json.dumps(obj=processed_obj, ensure_ascii=False, indent=4, encoding='utf-8')
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    print str_json


def DeteleTemporaryFile():
    os.remove('/analysis_data/received.json')


def MergeAnalyzedData(path_received_data, path_analyzed_data, keyname="index"):

    documents_received = io_operator.JsonOperator(path_received_data).load_json()
    documents_analyzed = io_operator.JsonOperator(path_analyzed_data).load_json()

    documents_updated = []
    for sentenceIndex, sentence in enumerate(documents_received["inputArray"]):
        if sentenceIndex == 0: keyNumber = '0'
        else: keyNumber = unicode(sentenceIndex)

        document = { "analyzed": documents_analyzed[keyNumber] }
        document["original"] = sentence

        documents_updated.append(document)

    return documents_updated



def __TestDataReveive():

    abs_path = os.path.abspath(sys.argv[0])
    abs_path_dir = os.path.dirname(abs_path)
    sys.path.append(abs_path_dir)
    os.chdir(abs_path_dir)

    res = StdIn()
    SaveTemporary(res, '../resources/received.json')


def __TestDictMerge():

    abs_path = os.path.abspath(sys.argv[0])
    abs_path_dir = os.path.dirname(abs_path)
    sys.path.append(abs_path_dir)
    os.chdir(abs_path_dir)

    path_resource_dir = "../resources/input.json"
    pathAnalyzed = "../resources/analyzed_data.json"

    document_updated = MergeAnalyzedData(path_resource_dir, pathAnalyzed)
    print document_updated

if __name__ == '__main__':
    __TestDictMerge()