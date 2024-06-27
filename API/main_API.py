from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from typing import List, Union
from main_function import *
import uvicorn
import logging
from datetime import datetime
import pytz
import torch

# logging.basicConfig(filename="Na.log", filemode='w')

# logger = logging.getLogger("Na")
# logger.setLevel(logging.DEBUG)
# file_handler = logging.FileHandler("Na.log")
# logger.addHandler(file_handler)
# total_done = 0
# total_error = 0

app = FastAPI()

class Item(BaseModel):
    url: str

def get_bd_time():
    bd_timezone = pytz.timezone("Asia/Dhaka")
    time_now = datetime.now(bd_timezone)
    current_time = time_now.strftime("%I:%M:%S %p")
    return current_time


async def process_item(item: Item):
    try:
        result = await mainDet(item.url)
        result = json.loads(result)
        return result
    finally:
        torch.cuda.empty_cache()
        pass

async def process_items(items: Union[Item, List[Item]]):
    print(type(items))
    if type(items)==list:
        coroutines = [process_item(item) for item in items]
        results = await asyncio.gather(*coroutines)
        print("multi : ",results)
    else:
        results = await process_item(items) # type: ignore
        print("single : ", results)
    return results



@app.get("/status")
async def status():
    return "AI Server in running"

@app.post("/nagad")
async def create_items(items: Union[Item, List[Item]]):
    try:
        # global total_done
        # total_done +=1
        results = await process_items(items)
        # print("Result Sent to User:", results)
        # print("###################################################################################################")
        # print(items)
        # print("Last Execution Time : ", get_bd_time())
        # logger.info(f"Time:{get_bd_time()}, Execution Done and Total Successfull Execution : {total_done}")
        return results
    except Exception as e:
        # global total_error
        # total_error += 1
        # logger.info(f"Time:{get_bd_time()}, Execution Failed and Total Failed Execution : {total_error}, Payload:{items}")
        # logger.error(str(e))
        return {"AI": f"Error: {str(e)}"}
    finally:
        # global total_done
        # total_done +=1
        # logger.info(f"Time:{get_bd_time()}, Execution Done and Total Successfull Execution : {total_done}, Payload:{items}")
        torch.cuda.empty_cache()
        pass

if __name__ == "__main__":
    try:
        # del nbrtuModel
        uvicorn.run(app, host="127.0.0.1", port=8000)
    finally:
        torch.cuda.empty_cache()

# python -m uvicorn main_API:app --reload
