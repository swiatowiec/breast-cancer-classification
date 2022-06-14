import yaml


class EdaConfig:
    def __init__(self, config_file):
        f = open(config_file, "r")
        params = yaml.safe_load(f)
        self.run_name = params["eda"]["run_name"]
        self.input_data_dir_path = params["eda"]["input_data_dir_path"]
        self.filetype = params["eda"]["filetype"]
        self.artifacts_dir_path = params["eda"]["artifacts_dir_path"]
        self.target_column = params["eda"]["target_column"]
        self.distribution_plot = params["eda"]["distribution_plot"]
        self.correlation_plot = params["eda"]["correlation_plot"]
