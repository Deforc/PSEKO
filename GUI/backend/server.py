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
  "latexCode": "\\documentclass{article}\n\\usepackage{color}\n\\begin{document}\nStyle: tree\n\n\\textbf{PROGRAM}\nWHILE $a \\neq 0 & b \\neq 0$ DO\nIF $a > b$ THEN\n$a \\gets a \\bmod b$\nELSE\n$b \\gets b \\bmod a$\nEND_IF\nEND_WHILE\n\\textcolor[RGB]{0,0,255}{Keywords are highlighted here}\n\\textcolor[RGB]{128,128,128}{Comments are highlighted here}\n\\end{document}"
}

# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)