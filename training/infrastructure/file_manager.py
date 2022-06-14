import pandas as pd
import glob
import json
import pickle
import os


class FileManager:
    def save_to_json(self, json_content, output_file):
        with open(output_file, 'w') as fd:
            return json.dump(json_content, fd)

    def read_from_json(self, file):
        with open(file, 'r') as fd:
            return json.load(fd)

    def save_to_pickle(self, obj, output_file):
        f = open(output_file, "wb")
        pickle.dump(obj, f)
        f.close()

    def read_from_pickle(self, input_file):
        if not os.path.isfile(input_file):
            return None
        f = open(input_file, "rb")
        obj = pickle.load(f)
        f.close()
        return obj
