import sys
import torch
import joblib
import numpy as np
import pandas as pd
from src.RNN_Price_prediction.config.configuration import ConfigurationManager
from src.RNN_Price_prediction.components.model_trainer import LSTMModel
from src.RNN_Price_prediction.components.model_evaluation import ModelEvaluation
from src.RNN_Price_prediction.data_access.yaho_finance import Connect_Yaho_finance
from logger import logging
from exception import MyException

class PredictionPipeline:
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.yf = Connect_Yaho_finance()

    async def predict(self, ticker: str):
        try:
            logging.info(f"Starting prediction for {ticker}")
            
            transform_config = self.config_manager.get_data_transformation_config()
            trainer_config = self.config_manager.get_model_trainer_config()
            eval_config = self.config_manager.get_model_evaluation_config()
            
            scaler = joblib.load(transform_config.scaler_path)
            
            model = LSTMModel(
                input_size=1, 
                hidden_size=trainer_config.hidden_size, 
                num_layers=trainer_config.num_layers, 
                output_size=trainer_config.output_size
            )
            model.load_state_dict(torch.load(trainer_config.trained_model_path))
            model.eval()
            
            data = await self.yf.fetch_data_by_tickes(ticker)
            
            close_cols = [col for col in data.columns if 'Close' in col]
            if not close_cols:
                raise Exception("No 'Close' column found in fetched data")
            
            target_col = close_cols[0]
            last_window_df = data[target_col].tail(trainer_config.window_size)
            last_window = last_window_df.values.reshape(-1, 1)
            
            if len(last_window) < trainer_config.window_size:
                raise Exception(f"Not enough data for prediction. Need {trainer_config.window_size} points, got {len(last_window)}")
            
            scaled_window = scaler.transform(last_window)
            input_tensor = torch.tensor(scaled_window, dtype=torch.float32).unsqueeze(0) # (1, window_size, 1)
            
            with torch.no_grad():
                prediction_scaled = model(input_tensor)
            
            prediction_val = scaler.inverse_transform(prediction_scaled.numpy())
            prediction = float(prediction_val[0, 0])
            
            evaluation = ModelEvaluation(config=eval_config)
            forecast_plot_path = evaluation.generate_forecast_plot(
                ticker=ticker,
                historical_data=last_window,
                prediction=prediction
            )
            
            logging.info(f"Prediction for {ticker}: {prediction}")
            return prediction, forecast_plot_path

        except Exception as e:
            raise MyException(e, sys)
