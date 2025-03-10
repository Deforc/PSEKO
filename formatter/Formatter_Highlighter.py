from enum import Enum

class TreeNode:
    class Type(Enum):
        TOKEN = 0
        NONTERMINAL = 1

    def __init__(self, type, attribute=None, children=None):
        self.type = type
        self.attribute = attribute  # Значение узла (если терминал)
        self.children = children if children is not None else []  # Дочерние узлы

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
        if node.type == TreeNode.Type.TOKEN:
            result.append(node.attribute)
        else:
            for child in node.children:
                result.append(self._format_line(child))
        return ' '.join(result)

    def _format_ladder(self, node, level=0):
        result = []
        indent = ' ' * 4 * level
        if node.type == TreeNode.Type.TOKEN:
            result.append(f"{indent}{node.attribute}")
        else:
            result.append(f"{indent}{node.attribute}:")
            for child in node.children:
                result.append(self._format_ladder(child, level + 1))
        return '\n'.join(result)

    def _format_tree(self, node, level=0):
        result = []
        indent = ' ' * 4 * level
        connector = '|-- ' if level > 0 else ''
        if node.type == TreeNode.Type.TOKEN:
            result.append(f"{indent}{connector}{node.attribute}")
        else:
            result.append(f"{indent}{connector}{node.attribute}")
            for child in node.children:
                result.append(self._format_tree(child, level + 1))
        return '\n'.join(result)

class Highlighter:
    def __init__(self, color_rules):
        self.color_rules = color_rules

    def highlight(self, text):
        highlighted_text = text
        for token_type, color in self.color_rules.items():
            highlighted_text = highlighted_text.replace(token_type, self._apply_color(token_type, color))
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
    # Создаем пример AST
    ast = TreeNode(
        type=TreeNode.Type.NONTERMINAL,
        attribute='root',
        children=[
            TreeNode(type=TreeNode.Type.TOKEN, attribute='A'),
            TreeNode(
                type=TreeNode.Type.NONTERMINAL,
                attribute='nonterminal',
                children=[
                    TreeNode(type=TreeNode.Type.TOKEN, attribute='B'),
                    TreeNode(type=TreeNode.Type.TOKEN, attribute='C')
                ]
            )
        ]
    )

    formatter = Formatter(style='ladder') #line tree ladder
    formatted_text = formatter.format(ast)
    print("Formatted Text:")
    print(formatted_text)

    # Определяем правила раскраски
    color_rules = {
        'A': 'red',
        'B': 'green',
        'C': 'blue',
        'nonterminal': 'yellow',
        'root': 'magenta'
    }

    highlighter = Highlighter(color_rules)
    highlighted_text = highlighter.highlight(formatted_text)
    print("\nHighlighted Text:")
    print(highlighted_text)