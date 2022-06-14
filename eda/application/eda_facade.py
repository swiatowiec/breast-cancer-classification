from domain.data_series import DataSeries
from domain.eda_service import EdaService
from infrastructure.file_manager import FileManager


class EdaFacade:
    def __init__(self,
                 artifacts_dir_path,
                 file_manager: FileManager,
                 discover_service: EdaService):
        self._artifacts_dir_path = artifacts_dir_path
        self._discover_service = discover_service
        self._file_manager = file_manager

    def discover(self,
                 input_data_dir_path: str,
                 filetype: str,
                 run_name: str):
        assert run_name is not None
        data_series = DataSeries.from_csv(file_manager=self._file_manager,
                                          input_data_dir_path=input_data_dir_path,
                                          filetype=filetype)

        params = self._file_manager.read_params()

        plots, plots_data = self._discover_service.plotter(
            data_series=data_series, input_params=params)

        DataSeries.to_png(plots=plots, file_manager=self._file_manager,
                          artifacts_dir_path=self._artifacts_dir_path)

        DataSeries.to_csv(plots_data=plots_data, file_manager=self._file_manager,
                          artifacts_dir_path=self._artifacts_dir_path)
