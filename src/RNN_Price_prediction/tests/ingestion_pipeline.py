import os
import sys
import asyncio

sys.path.append(os.getcwd())
from logger import *

from src.RNN_Price_prediction.components.data_ingestion import DataIngestion
from src.RNN_Price_prediction.config.configuration import ConfigurationManager

async def main():
    try:
        logging.info("Starting Data Ingestion Pipeline")
        
        config_manager = ConfigurationManager()
        data_ingestion_config = config_manager.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        
        await data_ingestion.initiate_data_ingestion(tickers=["AAPL"])
        
        logging.info("Data Ingestion Pipeline completed successfully")
        
    except Exception as e:
        logging.error(f"Data Ingestion Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
