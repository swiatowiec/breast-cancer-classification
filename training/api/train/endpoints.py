from dependency_injector.wiring import Provide, inject
from containers_config import TrainOrTestContainer


@inject
def perform_training(to_split_dir_path,
                     splitted_dir_path,
                     train_dataset_name,
                     test_dataset_name,
                     training_mode,
                     run_name,
                     test_size,
                     val_size,
                     random_state,
                     facade=Provide[TrainOrTestContainer.training_facade],
                     penalty=None,
                     c=None,
                     max_samples=None,
                     max_features=None,
                     n_estimators=None,
                     learning_rate=None,
                     ):
    facade.train_or_test(
        training_mode=training_mode,
        to_split_dir_path=to_split_dir_path,
        splitted_dir_path=splitted_dir_path,
        train_dataset_name=train_dataset_name,
        test_dataset_name=test_dataset_name,
        run_name=run_name,
        test_size=test_size,
        val_size=val_size,
        random_state=random_state,
        penalty=penalty,
        c=c,
        max_samples=max_samples,
        max_features=max_features,
        n_estimators=n_estimators,
        learning_rate=learning_rate,
    )
