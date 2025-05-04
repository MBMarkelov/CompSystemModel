from fastapi import FastAPI,File, UploadFile, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from L1.PyTasks.task2 import trends_analysis
from L2.PyTasks.ball import drop_ball
from L3.dichotomy import dichotomy_selection
from L3.gold_ratio import  golden_selection_scipy
from L4.main import get_plots
from L5.simpy_version.telephone_line import TelephoneLine
from L5.simpy_version.service_stantion import ServiceStation
import json
from fastapi import UploadFile, File
import matplotlib.pyplot as plt
import io
import base64
import threading
import asyncio



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
@app.post("/L5/telephone_line_simulation/")
async def phone_simulation_endpoint():
    global simulation_instance
    
    simulation_instance = TelephoneLine(sim_time=1000000, arrival_rate=0.95, service_time=1.0, seed=42)
    
    thread = threading.Thread(target=simulation_instance.run)
    thread.start()
    
    return {"message": "Telephone simulation started"}


@app.post("/L5/service_station_simulation")
async def service_station_endpoint(request: dict):
    """Запускает симуляцию и возвращает начальные результаты"""
    global simulation_instance

    sim_time_hours = 1000
    arrival_rate = 0.95
    service_time = 1.0
    n_posts = 3
    queue_limit = 5 if request.get("queue_limit") == "true" else None

    simulation_instance = ServiceStation(sim_time_hours, arrival_rate, service_time, n_posts, queue_limit=queue_limit)
    
    thread = threading.Thread(target=simulation_instance.run_simulation)
    thread.start()

    return {"message": "Simulation started"}


@app.websocket("/ws/telephone_line_simulation")
async def websocket_phone_simulation(websocket: WebSocket):
    """
    Веб-сокет, отправляющий клиенту обновления состояния симуляции.
    Клиент получает данные каждые 0.1 секунды.
    """
    await websocket.accept()
    try:
        while True:
            if simulation_instance is not None:
                data = simulation_instance.get_state()
                await websocket.send_json(data)
                if data.get("finished"):
                    break
            await asyncio.sleep(0.1)
    except Exception as e:
        print("WebSocket connection closed", e)
        
@app.websocket("/ws/service_station_simulation")
async def websocket_service_station_simulation(websocket: WebSocket):
    """
    Веб-сокет, отправляющий клиенту обновления состояния симуляции.
    Клиент получает данные каждые 0.1 секунды.
    """
    await websocket.accept()
    try:
        while True:
            if simulation_instance is not None:
                data = simulation_instance.get_state()
                await websocket.send_json(data)
                if data.get("total") == data.get("served") + data.get("lost"): 
                    break
            await asyncio.sleep(0.1)
    except Exception as e:
        print("WebSocket connection closed", e)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)