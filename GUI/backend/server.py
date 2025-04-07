from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Разрешенный домен фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Модель данных Pydantic (опционально, для валидации)
class RequestData(BaseModel):
    style: str
    text: str
    colorKeywords: str
    colorComment: str

# Эндпоинт для приема данных
@app.post("/api/latex")
async def compile_latex(request_data: RequestData):
    print("Received data:", request_data)
    return {
   "latexCode": "\\documentclass{article}\n\\usepackage[utf8]{inputenc}\n\\usepackage{algorithm}\n\\usepackage{algorithmic}\n\n\\begin{document}\n\n\\begin{algorithm}\n\\caption{Bubble Sort with Multi-Line Comment}\n\\begin{algorithmic}[1]\n    \\FOR{$i \\gets 0$ \\TO $n - 1$}\n        \\FOR{$j \\gets 0$ \\TO $n - i - 2$}\n            \\STATE \\textcolor{808080}{Line 1 of comment} \\STATE \\textcolor{808080}{Line 2 of comment}\n            \\IF{$arr[j] > arr[j + 1]$}\n                \\STATE \\textcolor{0000FF}{\\textsc{Swap}} $arr[j]$ and $arr[j + 1]$\n            \\ENDIF\n        \\ENDFOR\n    \\ENDFOR\n\\end{algorithmic}\n\\end{algorithm}\n\n\\end{document}"
}

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)