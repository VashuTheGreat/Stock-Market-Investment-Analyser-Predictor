import os
import sys
import pandas as pd
import numpy as np
import torch
import joblib
from sklearn.preprocessing import MinMaxScaler
from src.RNN_Price_prediction.entity.config_entity import DataTransformationConfig
from logger import logging
from exception import MyException

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def get_data_transformation_object(self):
        return self.scaler

    def initiate_data_transformation(self, data_path: str):
        try:
            logging.info(f"Starting data transformation for {data_path}")
            df = pd.read_csv(data_path, header=[0, 1], index_col=0)
            
            close_cols = [col for col in df.columns if col[1] == 'Close']
            
            if not close_cols:
                close_cols = [col for col in df.columns if 'Close' in str(col)]
                
            if not close_cols:
                raise Exception(f"No 'Close' column found in data. Columns: {df.columns}")
                
            target_data = df[close_cols[0]].values.reshape(-1, 1)
            
            target_data = target_data[~np.isnan(target_data).any(axis=1)].reshape(-1, 1)
            
            scaled_data = self.scaler.fit_transform(target_data)
            
            logging.info("Transformed data successfully")
            
            os.makedirs(self.config.root_dir, exist_ok=True)
            
            joblib.dump(self.scaler, self.config.scaler_path)
            
            torch.save(torch.tensor(scaled_data, dtype=torch.float32), self.config.transformed_data_path)
            
            logging.info(f"Saved scaler to {self.config.scaler_path} and transformed data to {self.config.transformed_data_path}")
            
            return self.config.transformed_data_path, self.config.scaler_path

        except Exception as e:
            raise MyException(e, sys)

    def create_sequences(self, data: torch.Tensor, window_size: int):
        X, y = [], []
        for i in range(len(data) - window_size):
            X.append(data[i:i+window_size])
            y.append(data[i+window_size])
        return torch.stack(X), torch.stack(y)
