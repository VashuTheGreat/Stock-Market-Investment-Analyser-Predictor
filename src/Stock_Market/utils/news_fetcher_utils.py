
import yfinance as yf

async def news_fetcher(name:str)->list[str]:
    news=[]
    result=yf.Search(name)
    # print(result.quotes)
    for i in result.news:
        news.append(i['title'])
    return news
