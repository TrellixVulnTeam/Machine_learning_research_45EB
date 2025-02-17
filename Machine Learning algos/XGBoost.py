# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 13:51:05 2018

@author: Shubham
"""

from sklearn.datasets import load_boston
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn.model_selection import train_test_split

boston = load_boston()

data = pd.DataFrame(boston.data)
data.columns = boston.feature_names
data['PRICE'] = boston.target

print(data.head())

X, y = data.iloc[:,:-1],data.iloc[:,-1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                    random_state=1)

xg_reg = xgb.XGBRegressor(objective='reg:linear', colsample_bytree=0.3, 
                          learning_rate=0.1, max_depth=5, alpha=10, 
                          n_estimators=10)

xg_reg.fit(X_train, y_train)
preds = xg_reg.predict(X_test)

print('predicting')
print(preds)

params = {"objective":"reg:linear",'colsample_bytree': 0.3,'learning_rate': 0.1,
                'max_depth': 5, 'alpha': 10}

data_dmatrix = xgb.DMatrix(data=X,label=y)
cv_results = xgb.cv(dtrain=data_dmatrix, params=params, nfold=3,
                    num_boost_round=50,early_stopping_rounds=10,metrics="rmse", as_pandas=True, seed=123)

print((cv_results["test-rmse-mean"]).tail(1))