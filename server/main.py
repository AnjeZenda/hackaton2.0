from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
import base64
import matplotlib.pyplot as plt, matplotlib
from pydantic import BaseModel
from typing import List, Dict
import numpy as np

matplotlib.use('agg')
app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HeaderElement(BaseModel):
    name: str
    required: bool
    label: str
    field: str
    align: str

class Data(BaseModel):
    header: List[HeaderElement]
    rows: List[Dict]

def render_data_string(string: str):
    if string == "":
        return 0
    if string.isdigit():
        return int(string)
    return string


@app.get('/')
def hello():
    return {'hello': 'world'}

@app.post('/api/linePlot')
def test(data: Data):
    
    
    header = [val.name for val in data.header]
    general_header = header[1:]
    rows = [list(map(render_data_string, list(row.values()))) for row in data.rows]

    plt.figure(figsize=(12,10))
    for row in rows:
        plt.plot(general_header, row[1:], label=row[0][:15].rstrip() + '...')
    
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.2, right=0.8)

    plt.title("Line-plot")
    plt.xlabel(header[0])
    plt.ylabel("Показатели")

    plt.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)

    img_data = base64.b64encode(img_buffer.read()).decode("utf-8")

    html_content = f'<h1>График</h1><img src="data:image/png;base64,{img_data}">'

    return HTMLResponse(content=html_content)

@app.post('/api/barChart')
def bar_chart(data: Data):
    header = [val.name for val in data.header]
    general_header = header[1:]
    rows = [list(map(render_data_string, list(row.values()))) for row in data.rows]
    bar_width = 0.08
    position = np.arange(len(general_header))
    plt.figure(figsize=(12,10))
    for row in rows:
        plt.bar(position, row[1:], bar_width, label=row[0][:15].rstrip() + '...')
        position = position + bar_width
    

    plt.xticks(position - (len(rows) + 1) * bar_width / 2, general_header , rotation=90)
    plt.subplots_adjust(bottom=0.2, right=0.8)

    plt.title("Bar-chart")
    plt.xlabel(header[0])
    plt.ylabel("Показатели")

    plt.legend(loc="center left", bbox_to_anchor=(1.0, 0.5))

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)

    img_data = base64.b64encode(img_buffer.read()).decode("utf-8")

    html_content = f'<h1>График</h1><img src="data:image/png;base64,{img_data}">'

    return HTMLResponse(content=html_content)
