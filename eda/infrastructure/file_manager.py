import os
import glob
import pandas as pd
import json
from config import EdaConfig

class FileManager:
    def read_files_in_folder(self, path, filetype):
        data_from_files = []
        for file_path in glob.glob('{}/*.{}'.format(path, filetype)):
            if file_path.endswith(filetype):
                data_from_files.append(pd.read_csv(file_path))
        return pd.concat(data_from_files)

    def save_data(self, data, output_data_dir_path, output_file_name, filetype):
        if filetype == 'csv':
            return data.to_csv(os.path.join(output_data_dir_path, output_file_name))
        else:
            raise Exception('Unsupported filetype')

    def save_to_json(self, json_content, output_file):
        with open(output_file, 'w') as fd:
            return json.dump(json_content, fd)

    def read_from_json(self, input_file):
        if not os.path.isfile(input_file):
            with open(input_file, 'w') as fd:
                json.dump({}, fd)
            return {}
        with open(input_file, 'r') as fd:
            return json.load(fd)

    def read_params(self):
        config = EdaConfig("config.yaml")
        return config


    def clean_dir(self, path):
        files = glob.glob(path + "/*")
        for f in files:
            if os.path.isfile(f):
                os.remove(f)

    def save_to_png(self, plots, artifacts_dir_path, filetype):
        for key in plots:
            plots[key].write_image(os.path.join(
                artifacts_dir_path, key + filetype))

    def save_plot_data(self, df, name, artifacts_dir_path):
        return df.to_csv(os.path.join(artifacts_dir_path, name + '.csv'))
