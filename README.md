# Breast Cancer Prediction using classification

This repository enables to predict whether the cancer is benign or mailgnant.

This project was created in cooperation with PredictForce. Non-commercial usage of this code was allowed. The publication of this code is without prejudice to any NDA clause.

## Data

The dataset is provided by Breat Cancer Wisconsin (Diagnostic) Data Set and is available here: https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+%28Diagnostic%29

## How to run

The project consists of the three modules:

1. preprocessing
2. exploratory data analysis (EDA)
3. training

Each module can be run separately and the ways to run those modules are presented below.

**preprocessing module**

- run _run_preprocess_process.py_ file if you want to preprocess data for the first time (fit and transform process). This process will generate the metadata.

  The following fullfillment modes are available:

  1. mean
  2. median

- run _run_preprocess_server.py_ file if you want to preprocess the sample of data during the transform process. The previously generated metadata will be used.

**EDA module**

- run _run_eda_process.py_ to discover the dataset.

**training module**

- run _run_train_process.py_ to train choosen model.

The following models are available:

1. Logistic Regression with Grid Search (log_reg_grid_search)
2. Logistic Regression with RFE (log_reg_rfe)
3. Bagging ensemble (bagging)
4. Boosting ensemble (boosting)

- run _run_predict_server.py_ to predict target based on previously trained model
