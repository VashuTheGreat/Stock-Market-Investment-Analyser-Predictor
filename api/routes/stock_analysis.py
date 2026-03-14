from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from src.Stock_Market.pipelines.run_pipeline import RunPipeline
import sys
import os

router = APIRouter()

class TickerList(BaseModel):
    tickers: List[str]

@router.post("/analyze")
async def analyze_stocks(data: TickerList):
    try:
        pipeline = RunPipeline()
        analysis = await pipeline.give_analysis(ticker_list=data.tickers)
        return {"analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
