#-*- coding:utf-8 -*-
__author__ = 'kensuke-mi'

import io_operator
import sys
import MeCab
import logging
import subprocess
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

"""
Calls MeCab and split sentences into set of words.
"""

def __check_mecab_dict_path__(osType):

    if osType=="mac":
        mecab_dic_cmd = 'echo `mecab-config --dicdir`'
    elif osType=="centos":
        mecab_dic_cmd = "echo `/usr/local/bin/mecab-config --dicdir`"


    path_mecab_dict = subprocess.check_output( mecab_dic_cmd, shell=True  ).strip(u'\n')

    return path_mecab_dict


def __check_mecab_libexe__(osType):

    if osType=="mac":
        mecab_libexe_cmd = 'echo `mecab-config --libexecdir`'
    elif osType=="centos":
        mecab_libexe_cmd = "echo `/usr/local/bin/mecab-config --libexecdir`"

    path_mecab_libexe = subprocess.check_output( mecab_libexe_cmd, shell=True  ).strip(u'\n')

    return path_mecab_libexe


def __CompileUserdict(pathUserdict, osType="mac"):
    # 複合語辞書のコンパイルをする

    #userDictLines = [
    #    line.strip(u'\n')
    #    for line in codecs.open(pathUserdict, 'r', 'utf-8').readlines()
    #    if line[0] != u'#' and line != u'\n']

    path_mecab_dict = __check_mecab_dict_path__(osType)
    path_mecab_libexe = __check_mecab_libexe__(osType)

    cmCompileDict = u'{0}/mecab-dict-index -d {1}/ipadic -u {2} -f utf-8 -t utf-8 {3} > /dev/null'.format(path_mecab_libexe,
                                                                                                            path_mecab_dict,
                                                                                                            pathUserdict.replace("csv", "dict"),
                                                                                                            pathUserdict)
    logging.debug(msg="compiling mecab user dictionary with: {}".format(cmCompileDict))
    try:
        subprocess.call( cmCompileDict , shell=True )
    except OSError as e:
        logging.error('type:' + str(type(e)))
        logging.error('args:' + str(e.args))
        logging.error('message:' + e.message)
        sys.exit('Failed to compile mecab userdict. System ends')

    return pathUserdict.replace("csv", "dict")



def __CallMecab(pathUserDictCsv, pathNeologd, osType, mode='all'):
    """
    Mecabの呼び出すをする
    :return:
    """
    if mode == 'neologd':
        logging.debug('Use neologd additional dictionary')
        cmMecabInitialize = '-d {}'.format(pathNeologd)

    elif mode == 'all':
        logging.debug('Use neologd additional dictionary')
        pathUserDict = __CompileUserdict(pathUserDictCsv, osType)
        cmMecabInitialize = '-u {} -d {}'.format(pathUserDict, pathNeologd)


    cmMecabCall = "-Ochasen {}".format(cmMecabInitialize)
    logging.debug(msg="mecab initialized with {}".format(cmMecabCall))

    try:
        mecabObj = MeCab.Tagger(cmMecabCall)
    except Exception as e:
        logging.error(e.args)
        logging.error(e.message)
        logging.error(e.args)
        sys.exit("Possibly Path to userdict is invalid check the path")

    return mecabObj


def __feature_parser__(uni_feature, word_surface):
    """
    Parse the POS feature output by Mecab
    :param uni_feature unicode:
    :return ( (pos1, pos2, pos3), word_stem ):
    """
    list_feature_items = uni_feature.split(u',')
    pos1 = list_feature_items[0]
    pos2 = list_feature_items[1]
    pos3 = list_feature_items[2]
    tuple_pos = ( pos1, pos2, pos3 )

    # if without constraint(output is normal mecab dictionary like)
    if len(list_feature_items) == 9:
        word_stem = list_feature_items[6]
    # if with constraint(output format depends on Usedict.txt)
    else:
        word_stem = word_surface

    return tuple_pos, word_stem


def __split_mode_Ochasen_userdict__(sentence, mecabObj):
    """
    :param sentence:
    :param ins_mecab:
    :param list_stopword:
    :param list_pos_candidate:
    :return:  list [tuple (unicode, unicode)]
    """
    list_sentence_processed = []  # list to save word stem of posted contents
    # don't delete this variable. encoded_text protects sentence from deleting
    encoded_text = sentence.encode('utf-8')

    node = mecabObj.parseToNode(encoded_text)
    node = node.next
    while node.next is not None:
        word_surface = node.surface.decode('utf-8')
        tuple_pos, word_stem = __feature_parser__(node.feature.decode('utf-8'), word_surface)
        list_sentence_processed.append( (word_stem, tuple_pos) )

        node = node.next

    return list_sentence_processed


def __JsonSave(pathSave, documentObj):
    """

    :return:
    """
    logging.debug("analyzed document is saved at: {}".format(pathSave))
    io_operator.JsonOperator(pathSave, any_data=documentObj).write_json()


def __JsonLoad(documentPath):
    """

    :return:
    """
    documentObj = io_operator.JsonOperator(path_to_json=documentPath).load_json()
    return documentObj


def __SentenceExtractor__(documentObjects):
    sentences = [
        (index, fumanObject)
        for index, fumanObject in enumerate(documentObjects['inputArray'])
    ]
    return sentences


def __SentenceSpliter__(sentences, mecabObj):
    analyzedResults = {
        int(sentence[0]): __split_mode_Ochasen_userdict__(sentence[1], mecabObj)
        for sentence in sentences
    }
    return analyzedResults


def MecabWrapperMain(pathUserDictCsv, documentPath, pathAnalyzedData, osType="mac",
                     pathNeologd="/usr/local/lib/mecab/dic/mecab-ipadic-neologd/"):


    mecabObj = __CallMecab(pathUserDictCsv, pathNeologd, osType)

    documentObjects = __JsonLoad(documentPath)
    sentences = __SentenceExtractor__(documentObjects)
    analyzedResults = __SentenceSpliter__(sentences, mecabObj)

    __JsonSave(pathAnalyzedData, analyzedResults)
    logging.debug("analyzed result is saved into {}".format(pathAnalyzedData))

    return pathAnalyzedData


def __test():
    import os

    abs_path = os.path.abspath(sys.argv[0])
    abs_path_dir = os.path.dirname(abs_path)
    sys.path.append(abs_path_dir)
    os.chdir(abs_path_dir)

    pathUserDictCsv="../resources/termExtractDict.csv"
    pathNeologd="/usr/local/lib/mecab/dic/mecab-ipadic-neologd/"
    osType="mac"
    mecabObj = __CallMecab(pathUserDictCsv, pathNeologd, osType)

    documentPath = "../resources/input.json"
    documentObjects = __JsonLoad(documentPath)
    sentences = __SentenceExtractor__(documentObjects)
    analyzedResults = __SentenceSpliter__(sentences, mecabObj)


    pathAnalyzedData = "../resources/analyzed_data.json"
    __JsonSave(pathAnalyzedData, analyzedResults)


if __name__ == "__main__":
    __test()

