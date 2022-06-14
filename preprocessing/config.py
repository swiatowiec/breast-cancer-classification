import yaml


class PreprocesingConfig:
    def __init__(self, config_file):
        f = open(config_file, "r")
        params = yaml.safe_load(f)
        self.input_dir_path = params["preprocessing"]["input_dir_path"]
        self.output_dir_path = params["preprocessing"]["output_dir_path"]
        self.output_file_name = params["preprocessing"]["output_file_name"]
        self.metadata_dir_path = params["preprocessing"]["metadata_dir_path"]
        self.fulfillment_mode = params["preprocessing"]["fulfillment_mode"]
        self.columns_to_fulfill = params["preprocessing"]["columns_to_fulfill"].split(
            ',')
        self.target_column = params["preprocessing"]["target_column"].split(
            ',')
        self.n_components = params["preprocessing"]["n_components"]
        self.run_name = params["preprocessing"]["run_name"]
