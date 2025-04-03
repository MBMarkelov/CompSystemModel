from fastapi import FastAPI,File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from L1.PyTasks.task2 import trends_analysis
from L2.PyTasks.ball import drop_ball
from L3.dichotomy import dichotomy_selection
from L3.gold_ratio import  golden_selection_scipy
from L4.main import get_plots
import json
from fastapi import UploadFile, File
import matplotlib.pyplot as plt
import io
import base64


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

@app.get("/L3/golden_selection/")
async def extrema_endpoint():
    result = golden_selection_scipy()
    return JSONResponse(content=result)

@app.get("/L3/dichotomy_selection/")
async def analyze_endpoint():
    result = dichotomy_selection()
    return JSONResponse(content=result)

@app.get("/L4/frequensy_tests/")
def get_frequency_plots():
    """
    Эндпоинт для получения графиков частотного теста обоих генераторов.
    
    Возвращает:
      JSON с base64‑кодированными PNG изображениями графиков.
    """
    fig1, fig2 = get_plots()

    buf1 = io.BytesIO()
    fig1.savefig(buf1, format='png')
    buf1.seek(0)
    image1 = base64.b64encode(buf1.read()).decode('utf-8')
    plt.close(fig1)

    buf2 = io.BytesIO()
    fig2.savefig(buf2, format='png')
    buf2.seek(0)
    image2 = base64.b64encode(buf2.read()).decode('utf-8')
    plt.close(fig2)

    return {"multinomial_plot": image1, "cubic_plot": image2}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)