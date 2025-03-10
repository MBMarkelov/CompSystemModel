from fastapi import FastAPI,File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from L1.PyTasks.task1 import minimize_solution
from L1.PyTasks.task2 import trends_analysis
from L2.PyTasks.ball import drop_ball
import json
from fastapi import UploadFile, File


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/L1/PyTasks/task2/trends_analysis/")
async def upload_file(file: UploadFile = File(...)):
    file_path = f"/tmp/{file.filename}"  # временное хранилище
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    result = trends_analysis(file_path)  # анализируем тренды
    return JSONResponse(content=result)

@app.post("/L2/PyTasks/ball/drop_ball/")
async def ball_endpoint(data: dict):
    print(f"Received data: {data}")  # Логируем данные, которые приходят
    return {"image_url": drop_ball(json.dumps(data))}



#@app.post("/L1/trends_analysis/")
#async def trends_analysis(data: dict):
 #   result = minimaize_solution(json.dumps(data))
  #  return json.loads(result)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)