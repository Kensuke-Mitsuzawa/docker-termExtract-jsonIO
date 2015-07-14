__author__ = 'kensuke-mi'

import codecs
import json
import os

class InputOperator:

    def __init__(self, input_path, sep, extract_index=''):
        self.input_path = input_path
        self.sep = sep
        self.extract_index = extract_index


    def load_fobj(self):
        obj_file = codecs.open(self.input_path, 'r', 'utf-8')
        return obj_file


    def load_into_list(self):

        f_obj = codecs.open(self.input_path, 'r', 'utf-8').readlines()
        if self.extract_index != '':
            if self.sep=='':
                line_list = [line.strip(u'\n').strip(u'\r') for line in f_obj]
            else:
                line_list = [line.strip(u'\n').strip(u'\r').split(self.sep)[self.extract_index] for line in f_obj]
        else:
            line_list = [line.strip(u'\n').strip(u'\r').split(self.sep) for line in f_obj]

        return line_list


class OutputOperator:

    def __init__(self, list_data, output_path, sep):
        self.list_data = list_data
        self.output_path = output_path
        self.sep = sep


    def write_out_to_tsv(self):
        with codecs.open(self.output_path, 'w', 'utf-8') as f:
            [f.write(line) for line in self.list_data]




class JsonOperator:

    def __init__(self, path_to_json, any_data=''):
        self.path_to_json = path_to_json
        self.any_data = any_data


    def check_file_ext(self, check_ext='json'):
        filename, ext = os.path.splitext(os.path.basename(self.path_to_json))
        if ext == check_ext:
            return self.path_to_json
        else:
            new_file_name = '{}.{}'.format(filename, check_ext)
            path_prefix, old_file_name = os.path.split(self.path_to_json)
            new_file_path = os.path.join(path_prefix, new_file_name)
            return new_file_path


    def load_json(self):
        """
        RETURN: list [list [unicode]]
        """
        with codecs.open(self.path_to_json, 'r', 'utf-8') as obj_json:
            obj_json = json.load(obj_json)
        return obj_json


    def write_json(self):
        """
        write out to json
        """
        path_json_file = self.check_file_ext()
        with codecs.open(path_json_file, 'w', 'utf-8') as f:
            str_json = json.dumps(self.any_data, ensure_ascii=False, indent=4)
            f.write(str_json)