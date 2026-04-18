import fastapi
import logging
from src.RNN_Price_prediction.pipeline.training_pipeline import TrainingPipeline

router=fastapi.APIRouter()

@router.get("/returain")
async def returain():
    try:
        logging.info("Starting Full Model Training Pipeline")
        
        training_pipeline = TrainingPipeline()
        # Using some common stock tickers for the training pipeline
        tickers = ["AAPL", "NVDA", "MSFT", "GOOGL", "AMZN"]
        await training_pipeline.run_pipeline(tickers=tickers)
        
        logging.info("Model Training Pipeline completed successfully")
        print("\nSUCCESS: Model Training Pipeline completed.")
        return {"sucess":True,"message":"SUCCESS: Model Training Pipeline completed."}
        
    except Exception as e:
        if 'logging' in globals():
            logging.error(f"Model Training Pipeline failed: {e}")
        print(f"\nERROR: Model Training Pipeline failed: {e}")
        return {"sucess":False,"message":f"ERROR: Model Training Pipeline failed: {e}"}
