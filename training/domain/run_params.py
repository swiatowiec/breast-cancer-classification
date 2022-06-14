from domain.data_series import TrainingMode
from typing import List


class RunInputParametersDo:
    def __init__(self,
                 training_mode: TrainingMode,
                 val_size: float,
                 random_state: int,
                 penalty: List[str] = None,
                 c: List[float] = None,
                 max_samples: float = None,
                 max_features: float = None,
                 n_estimators: int = None,
                 learning_rate: float = None):
        self.training_mode = training_mode
        self.penalty = penalty
        self.c = c
        self.val_size = val_size
        self.random_state = random_state
        self.max_samples = max_samples
        self.max_features = max_features
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
