import sys
import os
import torch
import joblib
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from src.RNN_Price_prediction.entity.config_entity import ModelEvaluationConfig
from src.RNN_Price_prediction.components.model_trainer import LSTMModel
from logger import logging
from exception import MyException

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def generate_performance_plot(self):
        try:
            logging.info("Generating performance plot...")
            
            data = torch.load(self.config.transformed_data_path)
            scaler = joblib.load(self.config.scaler_path)
            
            model = LSTMModel(
                input_size=1,
                hidden_size=self.config.hidden_size,
                num_layers=self.config.num_layers,
                output_size=self.config.output_size
            )
            model.load_state_dict(torch.load(self.config.trained_model_path))
            model.eval()
            
            
            X, y = [], []
            for i in range(self.config.window_size, len(data)):
                X.append(data[i-self.config.window_size:i])
                y.append(data[i])
            
            X = torch.stack(X)
            y = torch.stack(y)
            
            with torch.no_grad():
                predictions_scaled = model(X)
            
            y_actual = scaler.inverse_transform(y.numpy())
            y_pred = scaler.inverse_transform(predictions_scaled.numpy())
            
            # Plot
            plt.figure(figsize=(12, 6))
            plt.plot(y_actual, label='Actual Price', color='blue', alpha=0.6)
            plt.plot(y_pred, label='Predicted Price', color='red', alpha=0.6)
            plt.title('Model Performance - Actual vs Predicted')
            plt.xlabel('Time Steps')
            plt.ylabel('Price')
            plt.legend()
            plt.grid(True)
            
            plt.savefig(self.config.performance_plot_path)
            plt.close()
            logging.info(f"Performance plot saved to {self.config.performance_plot_path}")
            
            return self.config.performance_plot_path

        except Exception as e:
            raise MyException(e, sys)

    def generate_forecast_plot(self, ticker: str, historical_data: np.ndarray, prediction: float):
        try:
            logging.info(f"Generating forecast plot for {ticker}...")
            
            plt.figure(figsize=(10, 5))
            
            history_len = min(50, len(historical_data))
            recent_history = historical_data[-history_len:]
            
            time_steps = np.arange(history_len)
            plt.plot(time_steps, recent_history, label='Recent History', color='blue')
            
            plt.scatter(history_len, prediction, color='green', label='Next Predicted Price', zorder=5)
            plt.plot([history_len-1, history_len], [recent_history[-1][0], prediction], color='green', linestyle='--')
            
            plt.title(f'Forecast for {ticker}')
            plt.xlabel('Time Step')
            plt.ylabel('Price')
            plt.legend()
            plt.grid(True)
            os.makedirs(os.path.dirname(self.config.forecast_plot_path), exist_ok=True)
            
            file_name = f"forecast_{ticker}.png"
            plot_path = os.path.join(os.path.dirname(self.config.forecast_plot_path), file_name)
            
            plt.savefig(plot_path)
            plt.close()
            logging.info(f"Forecast plot saved to {plot_path}")
            
            return plot_path

        except Exception as e:
            raise MyException(e, sys)
