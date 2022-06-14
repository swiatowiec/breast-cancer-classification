from dependency_injector import providers, containers
from domain.service import ModelService
from infrastructure.model_manager import ModelManager
from domain.facade import TrainOrTest, PredictFacade
from infrastructure.file_manager import FileManager
from domain.dataset_repository import DatasetRepository


class TrainOrTestContainer(containers.DeclarativeContainer):
    # Config
    config = providers.Configuration()

    # Service
    service = providers.Singleton(ModelService)

    # Infrastructure
    model_manager = providers.Singleton(ModelManager,
                                        artifacts_dir_path=config.artifacts_dir_path)
    file_manager = providers.Singleton(FileManager)
    dataset_repository = providers.Singleton(DatasetRepository)

    # Facade
    training_facade = providers.Singleton(TrainOrTest,
                                          service=service,
                                          file_manager=file_manager,
                                          dataset_repository=dataset_repository,
                                          model_manager=model_manager)


class PredictContainer(containers.DeclarativeContainer):
    # Config
    config = providers.Configuration()

    # Services
    model_service = providers.Singleton(ModelService)

    # Infrastructure
    model_manager = providers.Singleton(ModelManager,
                                        artifacts_dir_path=config.artifacts_dir_path)
    file_manager = providers.Singleton(FileManager)

    # Facade
    predicting_facade = providers.Singleton(PredictFacade,
                                            model_service=model_service,
                                            file_manager=file_manager,
                                            model_manager=model_manager
                                            )
