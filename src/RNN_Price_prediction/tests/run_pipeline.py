import sys
import os
import asyncio

# Add project root to sys.path
sys.path.append(os.getcwd())

from logger import *
from src.RNN_Price_prediction.pipeline.training_pipeline import TrainingPipeline
from src.RNN_Price_prediction.pipeline.prediction_pipeline import PredictionPipeline

async def main():
    ticker = "NVDA"
    try:
        logging.info(f"--- Running End-to-End Pipeline for {ticker} ---")
        
        print(f"Starting Training Pipeline for {ticker}...")
        train_pipeline = TrainingPipeline()
        model_path = await train_pipeline.run_pipeline(tickers=[ticker])
        print(f"Training completed! Model saved at: {model_path}")
        
        print(f"Starting Prediction Pipeline for {ticker}...")
        logging.info(f"Starting Prediction Pipeline for {ticker}...")
        prediction_pipeline = PredictionPipeline()
        prediction, plot_path = await prediction_pipeline.predict(ticker)
        
        print(f"\nSUCCESS! Predicted Next Close Price for {ticker}: ${prediction:.2f}")
        print(f"Forecast plot saved at: {plot_path}")

    except Exception as e:
        if 'logging' in globals():
            logging.error(f"Pipeline execution failed: {e}")
        print(f"\nERROR: Pipeline execution failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
