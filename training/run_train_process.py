import sys
from api.train.endpoints import perform_training
from containers_config import TrainOrTestContainer
from domain.data_series import TrainingMode
from config import TrainingConfig

if __name__ == '__main__':
    config = TrainingConfig("config.yaml")
    container = TrainOrTestContainer()

    container.wire(modules=[sys.modules[__name__]])

    container.config.artifacts_dir_path.from_value(config.artifacts_dir_path)

    perform_training(to_split_dir_path=config.to_split_dir_path,
                     splitted_dir_path=config.splitted_dir_path,
                     train_dataset_name=config.train_dataset_name,
                     test_dataset_name=config.test_dataset_name,
                     training_mode=TrainingMode[config.training_mode.upper()],
                     run_name=config.run_name,
                     test_size=config.test_size,
                     val_size=config.val_size,
                     random_state=config.random_state,
                     penalty=config.penalty,
                     c=config.c,
                     max_samples=config.max_samples if config.max_samples else None,
                     max_features=config.max_features if config.max_features else None,
                     n_estimators=config.n_estimators if config.n_estimators else None,
                     learning_rate=config.learning_rate if config.learning_rate else None,
                     )
