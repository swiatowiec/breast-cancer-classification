from dependency_injector import providers, containers
from application.eda_facade import EdaFacade
from domain.eda_service import EdaService
from infrastructure.file_manager import FileManager


class EdaContainer(containers.DeclarativeContainer):
    # Config
    config = providers.Configuration()

    # Services
    eda_service = providers.Singleton(EdaService)

    # Infrastructure
    file_manager = providers.Singleton(FileManager)

    # Facade
    eda_facade = providers.Singleton(EdaFacade,
                                     artifacts_dir_path=config.artifacts_dir_path,
                                     discover_service=eda_service,
                                     file_manager=file_manager)
