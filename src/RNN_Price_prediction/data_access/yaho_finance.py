import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from src.RNN_Price_prediction.contants import YAHU_FINANCE_FETCH_DATA_MONTHS

from utils.asyncHandler import asyncHandler

class Connect_Yaho_finance:
    def __init__(self,months:int=YAHU_FINANCE_FETCH_DATA_MONTHS):
        self.months=months
        pass

    @asyncHandler
    async def fetch_data_by_tickes(self,*tickers)->pd.DataFrame:
        start = datetime.now() - relativedelta(months=self.months)
        end = datetime.now()
        data = yf.download(
        tickers=tickers,
        start=start,
        end=end,
        group_by="ticker"
    )  
        return data





