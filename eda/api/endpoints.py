from dependency_injector.wiring import Provide, inject
from containers_config import EdaContainer


@inject
def perform_discover(input_data_dir_path,
                     filetype,
                     run_name,
                     facade=Provide[EdaContainer.eda_facade]):
    facade.discover(input_data_dir_path=input_data_dir_path,
                    filetype=filetype,
                    run_name=run_name
                    )