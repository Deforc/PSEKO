import sys
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from latex import build_pdf
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

class CompileRequest(BaseModel):
    filename: str
    latexCode: str

TEMP_DIR = "temp_latex"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/api/latex")
async def compile_latex(request_data: RequestData):
    print("Received data:", request_data)

    chosen_file = os.getcwd() + '\\GUI\\yaml\\' + extract_filename(request_data.text) + '.yaml'
    print("Chosen file: ", chosen_file)

    '''
    Здесь должна вызываться либа ИС ДСЛ
    И должен получаться ямлик, который мы будем загружать в форматтер
    '''
    formatter = Formatter(chosen_file, request_data.style, request_data.colorKeywords, request_data.colorComment)
    formatter_result = formatter.export_to_latex()

    return {'latexCode': formatter_result}

@app.post("/api/compile")
async def compile_latex_to_pdf(request_data: CompileRequest):
    try:
        # Создаем уникальное имя файла
        file_name = request_data.filename or "output"
        tex_file = os.path.join(TEMP_DIR, f"{file_name}.tex")
        pdf_file = os.path.join(TEMP_DIR, f"{file_name}.pdf")

        # Записываем LaTeX-код в .tex файл
        with open(tex_file, "w") as f:
            f.write(request_data.latexCode)

        # Компилируем LaTeX в PDF
        pdf = build_pdf(request_data.latexCode)
        pdf.save_to(pdf_file)

        # Возвращаем путь к PDF
        return {
            "texUrl": f"/static/{file_name}.tex",
            "pdfUrl": f"/static/{file_name}.pdf",
            "texFileName": f"{file_name}.tex",
            "pdfFileName": f"{file_name}.pdf"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error compiling LaTeX: {str(e)}")

from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory=TEMP_DIR), name="static")

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)