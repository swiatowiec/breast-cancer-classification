class DataSeries:
    def __init__(self, data):
        self.data = data

    def get_benign_columns(self, target_column):
        return self.data[(self.data[target_column] == 'B')]

    def get_malignant_columns(self, target_column):
        return self.data[(self.data[target_column] == 'M')]

    def get_corelation_matrix(self):
        return self.data.corr()

    @staticmethod
    def from_csv(file_manager, input_data_dir_path: str, filetype: str):
        data = file_manager.read_files_in_folder(input_data_dir_path, filetype)
        return DataSeries(data)

    @staticmethod
    def to_png(plots: dict, file_manager, artifacts_dir_path: str):
        file_manager.save_to_png(plots=plots,
                                 artifacts_dir_path=artifacts_dir_path,
                                 filetype='.png')

    @staticmethod
    def to_csv(plots_data: list, file_manager, artifacts_dir_path: str):
        for key in plots_data:
            file_manager.save_plot_data(df=plots_data[key], name=key,
                                        artifacts_dir_path=artifacts_dir_path)
