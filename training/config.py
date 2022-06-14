import yaml


class TrainingConfig:
    def __init__(self, config_file):
        f = open(config_file, "r")
        params = yaml.safe_load(f)
        self.to_split_dir_path = params["training"]["to_split_dir_path"]
        self.splitted_dir_path = params["training"]["splitted_dir_path"]
        self.train_dataset_name = params["training"]["train_dataset_name"]
        self.test_dataset_name = params["training"]["test_dataset_name"]
        self.artifacts_dir_path = params["training"]["artifacts_dir_path"]
        self.training_mode = params["training"]["training_mode"]
        self.test_size = params["training"]["test_size"]
        self.val_size = params["training"]["val_size"]
        self.random_state = params["training"]["random_state"]
        self.penalty = params["training"]["penalty"].split(',')
        self.c = params["training"]["c"].split(',')
        self.max_samples = params["training"]["max_samples"]
        self.max_features = params["training"]["max_features"]
        self.n_estimators = params["training"]["n_estimators"]
        self.learning_rate = params["training"]["learning_rate"]
        self.run_name = params["training"]["run_name"]
