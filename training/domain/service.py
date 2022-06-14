from domain.data_series import DataSeries, TrainingMode
from domain.run_params import RunInputParametersDo
from sklearn.metrics import confusion_matrix
from domain.model_repository import get_boosting_ensemble, get_bagging_ensemble, get_log_reg_gridsearch_model, get_log_reg_rfe_model, LogRegGridSearch, LogRegRfe, Bagging, Boosting
from domain.model_repository import Model

class ModelService:
    def train(self,
              data_series: DataSeries,
              input_params=RunInputParametersDo) -> (
            DataSeries):
        model = self._model_selection(input_params=input_params)
        X, y = data_series.get_featues_and_target()
        trained_model = model.train(X, y)
        model.generate_confusion_matrix(trained_model=trained_model)
        metrics = model.create_metrics()
        roc_curve = model.create_ROC_curve_plot()
        return trained_model, metrics, roc_curve

    def test(self,
             data_series: DataSeries, model: (LogRegRfe or LogRegGridSearch or Bagging or Boosting)
             ) -> DataSeries:
        X, y = data_series.get_featues_and_target()
        prediction = data_series.test(model, X)
        model_obj = Model()
        cm = confusion_matrix(y, prediction)
        metrics = model_obj.create_metrics(cm)
        roc_curve = model_obj.create_ROC_curve_plot(cm)
        return metrics, roc_curve

    def predict(self,
                data_series: DataSeries, model: (LogRegRfe or LogRegGridSearch or Bagging or Boosting)
                ) -> DataSeries:
        predicted = data_series.predict(model)
        return predicted

    def _model_selection(self,
                         input_params: RunInputParametersDo
                         ) -> LogRegRfe or LogRegGridSearch or Bagging or Boosting:
        if input_params.training_mode == TrainingMode.LOG_REG_GRID_SEARCH:
            return get_log_reg_gridsearch_model(penalty=input_params.penalty,
                                                c=input_params.c,
                                                val_size=input_params.val_size,
                                                random_state=input_params.random_state)

        if input_params.training_mode == TrainingMode.LOG_REG_RFE:
            return get_log_reg_rfe_model(val_size=input_params.val_size,
                                         random_state=input_params.random_state)

        if input_params.training_mode == TrainingMode.BAGGING:
            return get_bagging_ensemble(val_size=input_params.val_size,
                                        random_state=input_params.random_state,
                                        max_samples=input_params.max_samples,
                                        max_features=input_params.max_features,
                                        n_estimators=input_params.n_estimators)

        if input_params.training_mode == TrainingMode.BOOSTING:
            return get_boosting_ensemble(val_size=input_params.val_size,
                                         random_state=input_params.random_state,
                                         n_estimators=input_params.n_estimators,
                                         learning_rate=input_params.learning_rate)

        else:
            raise Exception(
                '{} training mode is not supported!'.format(input_params.training_mode))
