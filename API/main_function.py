import json
from PIL import Image
from aiohttp import ClientSession
from io import BytesIO
import asyncio
from Data.model import obb,pose
from angle_function import *

async def getImage(img_url, session):
    async with session.get(img_url) as response:
        img_data = await response.read()
        return BytesIO(img_data)

async def obb_detection(model,img_content, confidence=0.1):
    img = Image.open(img_content)
    result = model(img,device=0,conf=confidence)
    obb_points = json.loads(json.dumps((result[0].obb.xyxyxyxy.cpu().numpy().astype(int)).tolist()))
    return obb_points


async def pose_detection(model,img_content,confidence=0.1):
    img = Image.open(img_content)
    result = model(img,device=0,conf=confidence)
    pose_points = json.loads(json.dumps((result[0].keypoints.xy.cpu().numpy().astype(int)).tolist()))
    return pose_points


async def mainDet(url):
    async with ClientSession() as session:
        image = await asyncio.create_task(getImage(url, session))
        
        Tasks = [
                    asyncio.create_task(obb_detection(obb, image)),
                    asyncio.create_task(pose_detection(pose, image))
                ]
        
        OBB, POSE = await asyncio.gather(*Tasks)
        result = json.dumps(CenterAndAngle(OBB, POSE))
        return result