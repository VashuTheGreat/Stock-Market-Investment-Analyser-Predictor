from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api.routes import stock_analysis, rnn_prediction
import os

app = FastAPI(title="Stock Market Investment Analyser & Predictor API")

templates = Jinja2Templates(directory="api/templates")
app.mount("/static", StaticFiles(directory="api/static"), name="static")


app.mount("/artifacts", StaticFiles(directory="artifacts"), name="artifacts")

app.include_router(stock_analysis.router, prefix="/stock_market", tags=["Analysis"])
app.include_router(rnn_prediction.router, prefix="/rnn", tags=["Prediction"])

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



