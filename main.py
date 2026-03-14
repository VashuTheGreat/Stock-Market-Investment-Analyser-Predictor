from dotenv import load_dotenv
load_dotenv()

import sys
import os
import io

# Fix unicode encoding for windows console
# if sys.stdout.encoding != 'utf-8':
#     sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from api.main import app
import uvicorn

if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
























