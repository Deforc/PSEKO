import sys
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from utils.extractor import extract_filename, get_yaml_file_path

sys.path.append(os.getcwd())
from formatter.Formatter import Formatter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class RequestData(BaseModel):
    style: str
    text: str
    colorKeywords: str
    colorComment: str

@app.post("/api/latex")
async def compile_latex(request_data: RequestData):
    print("Received data:", request_data)
    chosen_file = extract_filename(request_data.text) + '.yaml'
    print("Chosen file: ", chosen_file)
    '''
    Здесь должна вызываться либа ИС ДСЛ
    И должен получаться ямлик, который мы будем загружать в форматтер
    '''

    '''
    Здесь создание и вызов форматтера
    '''

    formatter = Formatter(chosen_file, request_data.style, request_data.colorKeywords, request_data.colorComment)
    formatter_result = formatter.export_to_latex()

    '''
    Здесь вызов хайлайтера
    '''

    '''
    Здесь вызов паблишера
    '''

    '''
    Здесь ретёрним респонс с результатом паблишера
    '''
    return {'latexCode': formatter_result}
# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)