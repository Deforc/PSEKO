from fastapi import FastAPI, HTTPException
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

import sys
import os

sys.path.append(os.getcwd())
from formatter.Formatter_Highlighter import Formatter, create_highlighter

app = FastAPI()


class NodeType(str, Enum):
    NONTERMINAL = "NONTERMINAL"
    TERMINAL = "TERMINAL"


# Модель TreeNode
class TreeNode(BaseModel):
    type: NodeType
    nonterminal_type: Optional[str] = None
    attribute: Optional[str] = None
    value: Optional[str] = None
    children: Optional[List['TreeNode']] = []

    class Config:
        orm_mode = True


TreeNode.update_forward_refs()


# Ручка для обработки AST
@app.post("/api/latex")
async def process_ast(data: dict):
    try:
        # Преобразуем AST в строку (предполагая, что это нужно для форматирования)
        ast_string = data.get("text")
        if not ast_string:
            raise ValueError("Строка AST не найдена в запросе")

        # Преобразуем строку в объект TreeNode
        ast_object = parse_ast_from_string(ast_string)

        # Настройки форматирования и раскраски
        style = 'tree'  # line/ladder/tree
        color_rules = {keyword: 'blue' for keyword in KEYWORDS}

        # Создаем форматтер и подсветчик
        formatter = Formatter(style=style)
        highlighter = create_highlighter(style, color_rules)

        # Форматируем и раскрашиваем текст
        formatted_text = formatter.format(ast_object)
        highlighted_text = highlighter.highlight(formatted_text)
        numbered_text = formatter.add_line_numbers(highlighted_text)

        # Возвращаем результат
        return {"result": numbered_text}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка обработки AST: {str(e)}")


# Ключевые слова для раскраски
KEYWORDS = [
    'IF', 'THEN', 'ELSE', 'ELSEIF', 'END_IF',
    'FOR', 'DO', 'END_FOR', 'REPEAT', 'UNTIL',
    'WHILE', 'END_WHILE', 'FUNC', 'END_FUNC',
    'PROC', 'END_PROC', 'ITERATOR', 'END_ITERATOR',
    'INPUT', 'OUTPUT', 'GOTO', 'ARRAY', 'STRUCT',
    'SELECT', 'YIELD', 'RETURN', 'NEXT', 'FROM', 'TO', 'IN'
]

def parse_ast_from_string(ast_string: str) -> TreeNode:
    """
    Парсит строку в объект TreeNode.
    """
    # Создаем безопасный контекст для выполнения кода
    allowed_globals = {
        "TreeNode": TreeNode,
        "NodeType": NodeType,
        "__builtins__": {}
    }

    try:
        # Выполняем строку в безопасном контексте
        ast_object = eval(ast_string, allowed_globals, {})
        if not isinstance(ast_object, TreeNode):
            raise ValueError("Результат выполнения строки не является объектом TreeNode")
        return ast_object
    except Exception as e:
        raise ValueError(f"Ошибка при парсинге строки AST: {str(e)}")
