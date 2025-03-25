import xgboost as xgb
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from typing import Tuple

class CLVPredictor:
    def __init__(self, n_splits: int = 5):
        self.model = xgb.XGBRegressor(
            objective='reg:squarederror',
            n_estimators=1000,
            early_stopping_rounds=50
        )
        self.cv = TimeSeriesSplit(n_splits=n_splits)
        
    def train(self, X: pd.DataFrame, y: pd.Series) -> dict:
        """Train with time-series cross validation"""
        scores = []
        for train_idx, val_idx in self.cv.split(X):
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
            
            self.model.fit(
                X_train, y_train,
                eval_set=[(X_val, y_val)],
                verbose=False
            )
            scores.append(self.model.best_score)
            
        return {
            'avg_score': sum(scores)/len(scores),
            'feature_importance': self.model.feature_importances_
        }
