import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from src.RNN_Price_prediction.entity.config_entity import ModelTrainerConfig
from logger import logging
from exception import MyException

class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, output_size):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def initiate_model_trainer(self, transformed_data_path: str):
        try:
            logging.info(f"Starting model training for {transformed_data_path}")
            data = torch.load(transformed_data_path)
            
            X, y = [], []
            for i in range(len(data) - self.config.window_size):
                X.append(data[i:i+self.config.window_size])
                y.append(data[i+self.config.window_size])
            
            X, y = torch.stack(X), torch.stack(y)
            
            dataset = TensorDataset(X, y)
            loader = DataLoader(dataset, batch_size=self.config.batch_size, shuffle=True)
            
            model = LSTMModel(
                input_size=1, 
                hidden_size=self.config.hidden_size, 
                num_layers=self.config.num_layers, 
                output_size=self.config.output_size
            )
            
            criterion = nn.MSELoss()
            optimizer = optim.Adam(model.parameters(), lr=self.config.learning_rate)
            
            model.train()
            for epoch in range(self.config.epochs):
                for batch_X, batch_y in loader:
                    optimizer.zero_grad()
                    outputs = model(batch_X)
                    loss = criterion(outputs, batch_y)
                    loss.backward()
                    optimizer.step()
                
                if (epoch+1) % 10 == 0:
                    logging.info(f"Epoch [{epoch+1}/{self.config.epochs}], Loss: {loss.item():.6f}")

            os.makedirs(self.config.root_dir, exist_ok=True)
            torch.save(model.state_dict(), self.config.trained_model_path)
            
            logging.info(f"Saved trained model to {self.config.trained_model_path}")
            
            return self.config.trained_model_path

        except Exception as e:
            raise MyException(e, sys)
