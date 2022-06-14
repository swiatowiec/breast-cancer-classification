import sys
from api.endpoints import perform_discover
from containers_config import EdaContainer
from config import EdaConfig

if __name__ == '__main__':
    container = EdaContainer()
    config = EdaConfig("config.yaml")

    container.wire(modules=[sys.modules[__name__]])

    container.config.artifacts_dir_path.from_value(config.artifacts_dir_path)

    perform_discover(input_data_dir_path=config.input_data_dir_path,
                     filetype=config.filetype,
                     run_name=config.run_name)
