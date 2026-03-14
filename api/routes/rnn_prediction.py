from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict
from src.RNN_Price_prediction.pipeline.prediction_pipeline import PredictionPipeline
import sys
import os
import asyncio

router = APIRouter()

class TickerList(BaseModel):
    tickers: List[str]

class PredictionResult(BaseModel):
    ticker: str
    predicted_price: float
    graph_url: str

async def cleanup_images(image_paths: List[str]):
    """Delete temporary images after a delay to allow browser to load them."""
    await asyncio.sleep(15)
    for path in image_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
                print(f"Deleted temporary image: {path}")
        except Exception as e:
            print(f"Error deleting {path}: {e}")

@router.post("/predict")
async def predict_prices(data: TickerList, background_tasks: BackgroundTasks):
    try:
        pipeline = PredictionPipeline()
        results = []
        image_paths_to_cleanup = []
        
        for ticker in data.tickers:
            try:
                prediction, plot_path = await pipeline.predict(ticker=ticker)
                
                image_paths_to_cleanup.append(os.path.abspath(plot_path))
                
                graph_url = f"/{os.path.relpath(plot_path, start=os.getcwd()).replace('\\', '/')}"
                
                results.append(PredictionResult(
                    ticker=ticker,
                    predicted_price=prediction,
                    graph_url=graph_url
                ))
            except Exception as e:
                print(f"Error predicting for {ticker}: {e}")
                continue
        
        if image_paths_to_cleanup:
            background_tasks.add_task(cleanup_images, image_paths_to_cleanup)
                
        return {"predictions": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
