from infrastructure.dataset_repository import DatasetRepository
from domain.service import PreprocessingService
from domain.facade import PreprocessingFitTransformFacade, PreprocessingFitTransformArgs
from infrastructure.metadata import MetadataRepository
from config import PreprocesingConfig

if __name__ == '__main__':
    config = PreprocesingConfig("config.yaml")
    args = PreprocessingFitTransformArgs(input_dir_path=config.input_dir_path,
                                         output_dir_path=config.output_dir_path,
                                         output_file_name=config.output_file_name,
                                         fulfillment_mode=config.fulfillment_mode,
                                         run_name=config.run_name,
                                         columns_to_fulfill=config.columns_to_fulfill,
                                         target_column=config.target_column,
                                         n_components=config.n_components,
                                         )

    metadata_repository = MetadataRepository()
    dataset_repository = DatasetRepository()
    preprocessing_service = PreprocessingService()

    preprocess = PreprocessingFitTransformFacade(
        metadata_repository=metadata_repository,
        preprocessing_service=preprocessing_service,
        dataset_repository=dataset_repository)

    preprocess.fit_transform(args)
