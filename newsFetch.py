import yfinance as yf

def news_fetcher(name):
    news=[]
    result=yf.Search(name)
    # print(result.quotes)
    for i in result.news:
        news.append(i['title'])
    return news

if __name__=="__main__":
    print(news_fetcher("tesla"))
