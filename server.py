from fastapi import FastAPI,File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from L1.PyTasks.task1 import minimaize_solution
from L1.PyTasks.task2 import trends_analysis
from all_labs.lab_2.drown_balls import drown_balls
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/lab_1/get_trends/")
async def trends_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    with open("data.csv", "wb") as f:
        f.write(contents)
    return {"image_url": get_trends("data.csv")}

@app.get("L1/trend-analysis")
def get_trend_analysis():
    result = trends_analysis("/home/mark/Documents/github/CompSystemModel/L1/price.csv")
    return JSONResponse(content=result)

@app.post("/lab_1/maximize_profit/")
async def maximize_profit_endpoint(data: dict):
    result = minimaize_solution(json.dumps(data))
    return json.loads(result)

@app.post("/lab_2/drown_balls/")
async def drown_balls_endpoint(data: dict):
    return {"image_url": drown_balls(json.dumps(data))}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
