#-*- coding:utf-8 -*-
__author__ = 'kensuke-mi'

"""
1 json形式のファイルを読み込んで、１つの文書にする
2 文書ファイルに書き出して、term extractを呼び出す。outputを4:IPAdic辞書形式(コスト推定)で呼び出す
3 threshold以上の要素だけを選択し、mecab辞書に保存をする
"""
import json
import codecs
import os
import sys
import subprocess
import logging
import re
logging.basicConfig(level=logging.DEBUG)


def __JsonLoader(path_json_document):
    with codecs.open(path_json_document, mode='r', encoding='utf-8') as f:
        dic_fumans = json.load(f)

    return dic_fumans


def __TmpLocalSave(document, pathSave):
    with codecs.open(pathSave, 'w', 'utf-8') as f:
        f.write(document)

    return pathSave


def __PreProcessFumans(fuman_sentence):
    # 改行コードを消して、スペース一個に変える
    return fuman_sentence.replace(u'\r\n', u' ').replace(u'\n', u' ').replace(u'\r', u' ')


def __ConvertIntoDocument(dict_fumans):
    # １つの文書にする
    list_fumans = [__PreProcessFumans(fuman_object) for fuman_object in dict_fumans['inputArray']]

    fuman_big_document = u'\n'.join(list_fumans)

    return fuman_big_document


def __CallTermExtractor(documentFilePath, pathPerlDir, outOpt, options):
    pathTermExtractPL = os.path.join(pathPerlDir, "termextract_mecab.pl")

    cmTermExtract = "cat {} | {} --output {} {}".format(documentFilePath, pathTermExtractPL, outOpt, options)
    logging.debug(msg="TermExtractor Command: {}".format(cmTermExtract))

    try:
        res = subprocess.check_output( cmTermExtract , shell=True)
    except Exception as e:
        logging.error(e)
        logging.error(e.args)
        logging.error(e.message)
        sys.exit()

    return res


def __TermItemFormatter(item, threshold):
    wordScoreItem = re.split(pattern=r"\s+", string=item.decode("utf-8"))
    if len(wordScoreItem) == 2 and float(wordScoreItem[1]) >= threshold:
        return (wordScoreItem[0], float(wordScoreItem[1]))



def __TermResultParser(termResult, threshold=2.0):
    TermItems = [
        __TermItemFormatter(item, threshold)
        for item in termResult.split("\n")
        if __TermItemFormatter(item, threshold) != None
    ]

    return TermItems


def DictionaryConstructor(TermItems):
    formatter = lambda x: u"{},-1,-1,-400,名詞,一般,*,*,*,*,{},ふくごうご,フクゴウゴ,複合語\n".format(x[0], x[0])
    mecabDictFormat = [
        formatter(item)
        for item in TermItems
    ]
    return mecabDictFormat


def DictionaryOverWriter(pathSaveMecabDict, strMecabDictionary):
    try:
        lines = codecs.open(pathSaveMecabDict, 'r', 'utf-8').readlines()
    except Exception as e:
        logging.error(e)
        logging.error(e.message)
        logging.error(e.args)
        sys.exit()

    filteredLines = [
        dictLine
        for dictLine in strMecabDictionary
        if dictLine not in lines
    ]

    updatedLines = lines + filteredLines

    try:
        with codecs.open(pathSaveMecabDict, mode='w', encoding='utf-8') as f:
            f.writelines(updatedLines)
    except Exception as e:
        logging.error(e)
        logging.error(e.message)
        logging.error(e.args)
        sys.exit()

    return updatedLines


def main(pathJsonDocument, resourceDir, pathPerlDir = "../dev_files", threshold=2.0, options=''):

    outOpt = 1
    tmpDocumentPath = os.path.join(resourceDir, "tmp_document.txt")
    pathSaveMecabDict = os.path.join(resourceDir, "termExtractDict.csv")

    dict_fumans = __JsonLoader(pathJsonDocument)
    fuman_big_document = __ConvertIntoDocument(dict_fumans)

    tmpDocumentPath = __TmpLocalSave(fuman_big_document, tmpDocumentPath)

    termResult = __CallTermExtractor(tmpDocumentPath, pathPerlDir, outOpt, options)
    TermItems= __TermResultParser(termResult, threshold)
    strMecabDictionary = DictionaryConstructor(TermItems)

    DictionaryOverWriter(pathSaveMecabDict, strMecabDictionary)

    return pathSaveMecabDict


def test():
    abs_path = os.path.abspath(sys.argv[0])
    abs_path_dir = os.path.dirname(abs_path)
    sys.path.append(abs_path_dir)
    os.chdir(abs_path_dir)
    test_json_document = '../resources/input.json'
    dict_fumans = __JsonLoader(test_json_document)
    fuman_big_document = __ConvertIntoDocument(dict_fumans)
    tmpDocumentPath = '../resources/tmp_document.txt'
    tmpDocumentPath = __TmpLocalSave(fuman_big_document, tmpDocumentPath)
    pathPerlDir = "../../dev_files"
    outOpt = 1
    options = '--no_storage'

    termResult = __CallTermExtractor(tmpDocumentPath, pathPerlDir, outOpt, options)
    TermItems= __TermResultParser(termResult)
    strMecabDictionary = DictionaryConstructor(TermItems)
    pathSaveMecabDict = "../resources/termExtractDict.csv"
    updatedLines = DictionaryOverWriter(pathSaveMecabDict, strMecabDictionary)


if __name__=='__main__':
    test()
