from infrastructure.metadata import MetadataRepository
from infrastructure.dataset_repository import DatasetRepository
from service import PreprocessingService, PreprocessingOptions, MetadataDo
from pydantic import BaseModel
from typing import List, Dict


class PreprocessingFitTransformArgs(BaseModel):
    input_dir_path: str
    output_dir_path: str
    output_file_name: str
    fulfillment_mode: str
    run_name: str
    columns_to_fulfill: List[str]
    target_column: List[str]
    n_components: int


class PreprocessingFitTransformFacade:

    def __init__(self,
                 metadata_repository: MetadataRepository,
                 preprocessing_service: PreprocessingService,
                 dataset_repository: DatasetRepository,
                 ):
        self._metadata_repository = metadata_repository
        self._preprocessing_service = preprocessing_service
        self._dataset_repository = dataset_repository

    def fit_transform(self, args: PreprocessingFitTransformArgs):
        dataset = self._dataset_repository.read_dataset(
            input_dir_path=args.input_dir_path,
        )

        metadata_do = self._preprocessing_service.preprocess(
            dataset=dataset,
            fulfillment_mode=args.fulfillment_mode,
            columns_to_fulfill=args.columns_to_fulfill,
            target_column=args.target_column,
            n_components=args.n_components,
            )

        self._dataset_repository.save_dataset(
            dataset=dataset,
            output_dir_path=args.output_dir_path,
            output_file_name=args.output_file_name,
        )

        self._metadata_repository.save_metadata(
            metadata=metadata_do.to_dict(),
            run_name=args.run_name,
        )


class PreprocessingTransformFacade:
    def __init__(self,
                 metadata_repository: MetadataRepository,
                 preprocessing_service: PreprocessingService,
                 dataset_repository: DatasetRepository,
                 ):
        self._metadata_repository = metadata_repository
        self._preprocessing_service = preprocessing_service
        self._dataset_repository = dataset_repository

    def transform(self,
                  measurements: List[Dict],
                  run_name: str):

        measurements_series = self._dataset_repository.read_measurements(
            measurements)

        metadata_do = MetadataDo.from_dict(self._metadata_repository.get_metadata(
            run_name=run_name))

        preprocessing_options = PreprocessingOptions(
            fulfillment_mode=metadata_do.filler_metadata['filler_type'],
            columns_to_fulfill=list(
                metadata_do.filler_metadata['filler_value'].keys()),
            target_column=metadata_do.target_metadata['target_column'],
        )

        self._preprocessing_service.preprocess(
            dataset=measurements_series,
            preprocessing_options=preprocessing_options,
            metadata_do=metadata_do,
        )
