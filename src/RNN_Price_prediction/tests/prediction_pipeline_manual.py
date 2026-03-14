import os
import sys
import asyncio

sys.path.append(os.getcwd())

from logger import *
from src.RNN_Price_prediction.pipeline.prediction_pipeline import PredictionPipeline

async def main():
    try:
        logging.info("Starting Prediction Pipeline Manual Test")
        
        ticker = "AAPL" 
        prediction_pipeline = PredictionPipeline()
        
        print(f"Running prediction for {ticker}...")
        prediction = await prediction_pipeline.predict(ticker=ticker)
        
        logging.info(f"Prediction for {ticker} completed successfully")
        print(f"\nSUCCESS: Predicted Next Close Price for {ticker}: ${prediction:.2f}")
        
    except Exception as e:
        if 'logging' in globals():
            logging.error(f"Prediction Pipeline failed: {e}")
        print(f"\nERROR: Prediction Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
