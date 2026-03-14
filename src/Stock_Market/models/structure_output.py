

from pydantic import BaseModel,Field



class structuredOutput(BaseModel):
    suggestions:str=Field(description="suggestion summary of all the stocks in human readable formate and suggest him to invest in this company top company ok")
    stocks:dict[str,dict[str,str]]=Field(description="stocks to invest in along with the reasion in human readable formate summary type")    
