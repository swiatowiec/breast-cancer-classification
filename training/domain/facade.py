from domain.run_params import RunInputParametersDo
from infrastructure.file_manager import FileManager
from domain.service import ModelService
from infrastructure.model_manager import ModelManager
from domain.dataset_factory import DatasetFactory
from domain.data_series import TrainingMode
from typing import List, Dict
from domain.dataset_repository import DatasetRepository


class TrainOrTest:
    def __init__(self,
                 file_manager: FileManager,
                 dataset_repository: DatasetRepository,
                 service: ModelService,
                 model_manager: ModelManager):
        self._model_service = service
        self._file_manager = file_manager
        self._dataset_repository = dataset_repository
        self._model_manager = model_manager

    def train_or_test(self,
                      training_mode: TrainingMode,
                      to_split_dir_path: str,
                      splitted_dir_path: str,
                      train_dataset_name: str,
                      test_dataset_name: str,
                      run_name: str,
                      test_size: float,
                      val_size: float,
                      random_state: int,
                      penalty: List[str] = None,
                      c: List[float] = None,
                      max_samples: float = None,
                      max_features: float = None,
                      n_estimators: int = None,
                      learning_rate: float = None,
                      ):

        input_params = RunInputParametersDo(training_mode=training_mode,
                                            val_size=val_size,
                                            random_state=random_state,
                                            penalty=penalty,
                                            c=c,
                                            max_samples=max_samples,
                                            max_features=max_features,
                                            n_estimators=n_estimators,
                                            learning_rate=learning_rate,
                                            )

        assert run_name is not None
        dataset_factory = DatasetFactory(
            self._dataset_repository, test_size, random_state)
        dataset_factory.split_data(to_split_input_dir_path=to_split_dir_path,
                                   splitted_output_dir_path=splitted_dir_path)
        model = self._model_manager.read_from_pickle(file_manager=self._file_manager,
                                                     run_name=run_name)
        if model is None:
            train_data_series = dataset_factory.create_from_files(input_dir_path=splitted_dir_path,
                                                                  file_name=train_dataset_name
                                                                  )
            model, metrics, roc_curve = self._model_service.train(data_series=train_data_series,
                                                                  input_params=input_params)

            self._model_manager.persist_to_pickle(model=model,
                                                  file_manager=self._file_manager,
                                                  run_name=run_name)
                                                  
            self._model_manager.save_metrics(metrics=metrics,
                                             file_manager=self._file_manager,
                                             file_name='train')

            self._model_manager.save_ROC_curve_plot(plot=roc_curve,
                                                    file_manager=self._file_manager,
                                                    file_name='train')

        test_data_series = dataset_factory.create_from_files(input_dir_path=splitted_dir_path,
                                                             file_name=test_dataset_name
                                                             )
        metrics, roc_curve = self._model_service.test(data_series=test_data_series,
                                                      model=model)

        self._model_manager.save_metrics(metrics=metrics,
                                         file_manager=self._file_manager,
                                         file_name='test')

        self._model_manager.save_ROC_curve_plot(plot=roc_curve,
                                                file_manager=self._file_manager,
                                                file_name='test')


class PredictFacade:
    def __init__(self,
                 file_manager: FileManager,
                 model_service: ModelService,
                 model_manager: ModelManager):
        self._model_service = model_service
        self._file_manager = file_manager
        self._model_manager = model_manager

    def predict(self,
                measurements: List[Dict],
                run_name: str) -> List[int]:
        dataset_factory = DatasetFactory(self._file_manager)
        data_series = dataset_factory.create_from_dict_list(
            records=measurements)

        model = self._model_manager.read_from_pickle(file_manager=self._file_manager,
                                                     run_name=run_name)
        prediction = self._model_service.predict(data_series=data_series,
                                                 model=model)
        return prediction
