from enum import Enum
from dataclasses import dataclass

class NodeType(Enum):
    NONTERMINAL = 1
    TERMINAL = 2

@dataclass
class TreeNode:
    def __init__(self, node_type, nonterminal_type=None, attribute=None, value=None, children=None):
        self.type = node_type
        self.nonterminal_type = nonterminal_type
        self.attribute = attribute
        self.value = value  # Новое поле value
        self.children = children if children is not None else []  # Инициализация children

class Formatter:
    def __init__(self, style='line'):
        self.style = style

    def format(self, ast):
        if self.style == 'line':
            return self._format_line(ast)
        elif self.style == 'ladder':
            return self._format_ladder(ast)
        elif self.style == 'tree':
            return self._format_tree(ast)
        else:
            raise ValueError("Unsupported style")

    def _format_line(self, node):
        result = []
        if node.type == NodeType.TERMINAL:
            result.append(node.value if node.value is not None else node.attribute)
        else:
            for child in node.children:
                result.append(self._format_line(child))
        return ' '.join(result)

    def _format_ladder(self, node, level=0):
        result = []
        indent = ' ' * 4 * level
        if node.type == NodeType.TERMINAL:
            result.append(f"{indent}{node.value if node.value is not None else node.attribute}")
        else:
            result.append(f"{indent}{node.nonterminal_type}:")
            for child in node.children:
                result.append(self._format_ladder(child, level + 1))
        return '\n'.join(result)

    def _format_tree(self, node, level=0):
        result = []
        indent = ' ' * 4 * level
        connector = '|-- ' if level > 0 else ''
        if node.type == NodeType.TERMINAL:
            result.append(f"{indent}{connector}{node.value if node.value is not None else node.attribute}")
        else:
            result.append(f"{indent}{connector}{node.nonterminal_type}")
            for child in node.children:
                result.append(self._format_tree(child, level + 1))
        return '\n'.join(result)

class Highlighter:
    def __init__(self, color_rules):
        self.color_rules = color_rules

    def highlight(self, text):
        highlighted_text = text
        for token, color in self.color_rules.items():
            highlighted_text = highlighted_text.replace(token, self._apply_color(token, color))
        return highlighted_text

    def _apply_color(self, text, color):
        # ANSI escape codes for colors
        colors = {
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'reset': '\033[0m'
        }
        return f"{colors[color]}{text}{colors['reset']}"

# Пример использования
if __name__ == "__main__":
    # Создаем пример AST для предоставленного кода
    ast = TreeNode(
        node_type=NodeType.NONTERMINAL,
        nonterminal_type='Program',
        children=[
            TreeNode(node_type=NodeType.TERMINAL, attribute='Assignment', value='z : 30'),
            TreeNode(
                node_type=NodeType.NONTERMINAL,
                nonterminal_type='IF',
                children=[
                    TreeNode(node_type=NodeType.TERMINAL, attribute='Condition', value='z == 15'),
                    TreeNode(node_type=NodeType.TERMINAL, attribute='THEN', value='THEN'),  # Добавлен THEN
                    TreeNode(node_type=NodeType.TERMINAL, attribute='Output', value='OUTPUT "z равно 15"'),
                    TreeNode(node_type=NodeType.TERMINAL, attribute='ELSE', value='ELSE'),  # Добавлен ELSE
                    TreeNode(node_type=NodeType.TERMINAL, attribute='Output', value='OUTPUT "z не равно 15"')
                ]
            ),
            TreeNode(
                node_type=NodeType.NONTERMINAL,
                nonterminal_type='FOR',
                children=[
                    TreeNode(node_type=NodeType.TERMINAL, attribute='Loop', value='i FROM 1 TO 3'),
                    TreeNode(node_type=NodeType.TERMINAL, attribute='DO', value='DO'),  # Добавлен DO
                    TreeNode(node_type=NodeType.TERMINAL, attribute='Output', value='OUTPUT "Итерация: " + i')
                ]
            )
        ]
    )

    formatter = Formatter(style='tree')
    formatted_text = formatter.format(ast)
    print("Formatted Text:")
    print(formatted_text)

    # Определяем правила раскраски для ключевых слов
    KEYWORDS = [
        'IF', 'THEN', 'ELSE', 'ELSEIF', 'END_IF',
        'FOR', 'DO', 'END_FOR', 'REPEAT', 'UNTIL',
        'WHILE', 'END_WHILE', 'FUNC', 'END_FUNC',
        'PROC', 'END_PROC', 'ITERATOR', 'END_ITERATOR',
        'INPUT', 'OUTPUT', 'GOTO', 'ARRAY', 'STRUCT',
        'SELECT', 'YIELD', 'RETURN', 'NEXT', 'FROM', 'TO', 'IN'
    ]

    # Создаем правила раскраски: все ключевые слова красятся в красный
    color_rules = {keyword: 'red' for keyword in KEYWORDS}

    highlighter = Highlighter(color_rules)
    highlighted_text = highlighter.highlight(formatted_text)
    print("\nHighlighted Text:")
    print(highlighted_text)