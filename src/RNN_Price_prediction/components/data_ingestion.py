import os
import sys
import pandas as pd
from src.RNN_Price_prediction.entity.config_entity import DataIngestionConfig
from src.RNN_Price_prediction.data_access.yaho_finance import Connect_Yaho_finance
from logger import logging
from exception import MyException

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        self.yf = Connect_Yaho_finance()

    async def initiate_data_ingestion(self, tickers: list):
        logging.info(f"Entered initiate_data_ingestion for tickers: {tickers}")
        try:
            data = await self.yf.fetch_data_by_tickes(*tickers)
            
            logging.info(f"Data fetched successfully. Shape: {data.shape}")
            
            os.makedirs(os.path.dirname(self.config.raw_data_path), exist_ok=True)
            data.to_csv(self.config.raw_data_path, index=True)
            
            logging.info(f"Saved raw data to {self.config.raw_data_path}")
            
            return self.config.raw_data_path

        except Exception as e:
            raise MyException(e, sys)
