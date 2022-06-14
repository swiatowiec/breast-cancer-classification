from functools import lru_cache
from typing import List
from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier, RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFE
from sklearn.model_selection import GridSearchCV


class Model():
    def generate_confusion_matrix(self, trained_model):
        y_pred = trained_model.predict(self.X_val)
        self.cm = confusion_matrix(self.y_val, y_pred)

    def create_metrics(self, cm=None):
        if cm is None:
            tp = self.cm[1, 1]
            fn = self.cm[1, 0]
            fp = self.cm[0, 1]
            tn = self.cm[0, 0]
        else:
            tp = cm[1, 1]
            fn = cm[1, 0]
            fp = cm[0, 1]
            tn = cm[0, 0]

        accuracy = (tp+tn)/(tp+tn+fp+fn)
        precision = tp/(tp+fp)
        recall = tp/(tp+fn)
        F1_score = 2*(((tp/(tp+fp))*(tp/(tp+fn)))/((tp/(tp+fp))+(tp/(tp+fn))))
        return {'accuracy': accuracy, "precision": precision,
                "recall": recall, 'F1_score': F1_score}

    def create_ROC_curve_plot(self, cm=None):
        if cm is None:
            fp = int(self.cm[0, 1])
            tp = int(self.cm[1, 1])
        else:
            fp = int(cm[0, 1])
            tp = int(cm[1, 1])
        return {'fp': fp, 'tp': tp}


class LogRegGridSearch(Model):
    def __init__(self,
                 penalty: List[str],
                 c: List[float],
                 val_size: float,
                 random_state: int):
        self.penalty = penalty
        self.c = c
        self.val_size = val_size
        self.random_state = random_state

    def train(self, X, y):
        X_train, self.X_val, y_train, self.y_val = train_test_split(X,
                                                                    y,
                                                                    test_size=self.val_size,
                                                                    random_state=self.random_state)
        log_clf = LogisticRegression(random_state=self.random_state)
        param_grid = {
            'penalty': self.penalty,
            'C': self.c
        }
        grid_search_cv = GridSearchCV(estimator=log_clf,
                                      param_grid=param_grid,
                                      scoring='accuracy',
                                      verbose=1,
                                      n_jobs=-1)
        grid_search_cv.fit(X_train, y_train)

        best_parameters = grid_search_cv.best_params_

        model_to_train = LogisticRegression(C=best_parameters['C'],
                                            penalty=best_parameters['penalty'],
                                            random_state=self.random_state)
        trained_model = model_to_train.fit(X_train,
                                           y_train)

        return trained_model


class LogRegRfe(Model):
    def __init__(self,
                 val_size: float,
                 random_state: int):
        self.val_size = val_size
        self.random_state = random_state

    def train(self, X, y):
        logreg = LogisticRegression()
        model_to_train = RFE(logreg)
        X_train, self.X_val, y_train, self.y_val = train_test_split(X,
                                                                    y,
                                                                    test_size=self.val_size,
                                                                    random_state=self.random_state)
        trained_model = model_to_train.fit(X_train,
                                           y_train)
        return trained_model


class Bagging(Model):
    # https://machinelearningmastery.com/bagging-ensemble-with-python/
    def __init__(self,
                 val_size: float,
                 random_state: int,
                 max_samples: float,
                 max_features: float,
                 n_estimators: int):
        self.max_samples = max_samples
        self.max_features = max_features
        self.n_estimators = n_estimators
        self.val_size = val_size
        self.random_state = random_state

    def train(self, X, y):
        random_forest = RandomForestClassifier()
        X_train, self.X_val, y_train, self.y_val = train_test_split(X,
                                                                    y,
                                                                    test_size=self.val_size,
                                                                    random_state=self.random_state)
        model_to_train = BaggingClassifier(
            base_estimator=random_forest, max_samples=self.max_samples, max_features=self.max_features, n_estimators=self.n_estimators)
        trained_model = model_to_train.fit(X_train, y_train)
        return trained_model


class Boosting(Model):
    def __init__(self,
                 val_size: float,
                 random_state: int,
                 n_estimators: int,
                 learning_rate: float):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.val_size = val_size
        self.random_state = random_state

    def train(self, X, y):
        random_forest = RandomForestClassifier()
        X_train, self.X_val, y_train, self.y_val = train_test_split(X,
                                                                    y,
                                                                    test_size=self.val_size,
                                                                    random_state=self.random_state)
        model_to_train = AdaBoostClassifier(
            base_estimator=random_forest,
            n_estimators=self.n_estimators,
            learning_rate=self.learning_rate)
        trained_model = model_to_train.fit(X_train, y_train)
        return trained_model


@ lru_cache()
def get_log_reg_gridsearch_model(penalty: List[str],
                                 c: List[float],
                                 val_size: float,
                                 random_state: int):
    return LogRegGridSearch(penalty=penalty,
                            c=c,
                            val_size=val_size,
                            random_state=random_state)


@ lru_cache()
def get_log_reg_rfe_model(val_size: float,
                          random_state: int):
    return LogRegRfe(val_size=val_size,
                     random_state=random_state)


@ lru_cache()
def get_bagging_ensemble(val_size: float,
                         random_state: int,
                         max_samples: float,
                         max_features: float,
                         n_estimators: int):
    return Bagging(val_size=val_size,
                   random_state=random_state,
                   max_samples=max_samples,
                   max_features=max_features,
                   n_estimators=n_estimators)


@ lru_cache()
def get_boosting_ensemble(val_size: float,
                          random_state: int,
                          n_estimators: int,
                          learning_rate: float):
    return Boosting(val_size=val_size,
                    random_state=random_state,
                    n_estimators=n_estimators,
                    learning_rate=learning_rate)
