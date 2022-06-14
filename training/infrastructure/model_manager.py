import os.path


class ModelManager():
    def __init__(self, artifacts_dir_path: str):
        self._artifacts_dir_path = artifacts_dir_path

    def save_metrics(self, metrics, file_manager, file_name):
        file_manager.save_to_json(metrics, os.path.join(
            self._artifacts_dir_path, file_name + "_scores.json"))

    def save_ROC_curve_plot(self, plot, file_manager, file_name):
        file_manager.save_to_json(
            plot, os.path.join(self._artifacts_dir_path, file_name + "_ROC_curve.json"))

    def persist_to_pickle(self, model, file_manager, run_name):
        file_manager.save_to_pickle(model, os.path.join(
            self._artifacts_dir_path, "model.pkl"))

    def read_from_pickle(self, file_manager, run_name):
        return file_manager.read_from_pickle(
            os.path.join(self._artifacts_dir_path, run_name + ".pkl"))
