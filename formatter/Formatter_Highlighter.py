from enum import Enum
from dataclasses import dataclass
import re

# Определение типов узлов
class NodeType(Enum):
    NONTERMINAL = 1
    TERMINAL = 2

# Класс для представления узла дерева
@dataclass
class TreeNode:
    def __init__(self, node_type, nonterminal_type=None, attribute=None, value=None, children=None):
        self.type = node_type
        self.nonterminal_type = nonterminal_type
        self.attribute = attribute
        self.value = value
        self.children = children if children is not None else []

# Форматировщик для преобразования AST в различные стили
class Formatter:
    def __init__(self, style='tree'):
        self.style = style

    def format(self, ast):
        if self.style == 'line':
            return self._format_line(ast)
        elif self.style == 'ladder':
            return self._format_ladder(ast)
        elif self.style == 'tree':
            return self._format_tree(ast)  # Теперь возвращает только текст
        else:
            raise ValueError("Unsupported style")

    def _format_line(self, node):
        result = []
        if node.type == NodeType.TERMINAL:
            # Терминалы выводятся без раскраски, кроме SWAP
            value = node.value if node.value is not None else node.attribute
            if value == 'SWAP(arr[j], arr[j + 1])':
                result.append(f"\033[91m{value}\033[0m")  # Красный цвет
            else:
                result.append(value)  # Без раскраски
        else:
            # Нетерминалы выводятся без раскраски
            result.append(node.nonterminal_type)
            for child in node.children:
                result.append(self._format_line(child))
        return ' '.join(result)

    def _format_ladder(self, node, level=0):
        result = []
        indent = ' ' * 4 * level  # Базовый отступ

        if node.type == NodeType.TERMINAL:
            # Терминалы выводятся с базовым отступом
            value = node.value if node.value is not None else node.attribute
            result.append(f"{indent}{value}")
        else:
            # Если узел является FOR или IF
            if node.nonterminal_type in ['FOR', 'IF']:
                # Выводим открывающий узел (FOR или IF)
                result.append(f"{indent}{node.nonterminal_type}")

                # Обрабатываем дочерние элементы
                if node.children:
                    # Первый дочерний элемент (условие или действие) выводится на той же строке
                    if len(node.children) > 0:
                        child_line = self._format_ladder(node.children[0], 0)
                        result[-1] += f" {child_line}"

                    # Если следующий дочерний элемент имеет атрибут "DO" или "THEN", выводим его на той же строке
                    if len(node.children) > 1 and node.children[1].attribute in ['DO', 'THEN']:
                        child_line = self._format_ladder(node.children[1], 0)
                        result[-1] += f" {child_line}"

                    # Остальные дочерние элементы выводятся с новой строки и увеличенным отступом
                    for child in node.children[2:]:
                        if child.attribute in ['END_IF', 'END_FOR', 'END_WHILE', 'END_FUNC', 'END_PROC',
                                               'END_ITERATOR']:
                            # Закрывающие узлы выравниваются с открывающими
                            child_line = self._format_ladder(child, level)
                            result.append(child_line)
                        else:
                            # Остальные дочерние элементы выводятся с увеличенной табуляцией
                            child_line = self._format_ladder(child, level + 1)
                            result.append(child_line)
            else:
                # Для других нетерминалов просто добавляем отступ
                result.append(f"{indent}{node.nonterminal_type}")

                # Обрабатываем дочерние элементы
                for child in node.children:
                    if child.attribute in ['END_IF', 'END_FOR', 'END_WHILE', 'END_FUNC', 'END_PROC', 'END_ITERATOR']:
                        # Закрывающие узлы выравниваются с открывающими
                        child_line = self._format_ladder(child, level)
                        result.append(child_line)
                    else:
                        # Остальные дочерние элементы выводятся с увеличенной табуляцией
                        child_line = self._format_ladder(child, level + 1)
                        result.append(child_line)

        return '\n'.join(result)

    def _format_tree(self, node, level=0):
        result = []
        indent = ' ' * 4 * level
        connector = '|-- ' if level > 0 else ''

        if node.type == NodeType.TERMINAL:
            # Терминалы выводятся без окрашивания
            value = node.value if node.value is not None else node.attribute
            result.append(f"{indent}{connector}{value}")
        else:
            # Для нетерминальных узлов добавляем их тип (например, FOR, IF)
            # Исключаем окрашивание корневого узла "Program"
            if node.nonterminal_type == 'Program':
                result.append(f"{indent}{node.nonterminal_type}")
            else:
                result.append(f"{indent}{connector}{node.nonterminal_type}")

            # Обработка дочерних элементов
            for i, child in enumerate(node.children):
                if node.nonterminal_type in ['FOR', 'IF']:
                    # Если это первый дочерний элемент (например, условие или действие), выводим его на той же строке
                    if i == 0:
                        new_line = self._format_tree(child, 0)
                        result[-1] += f" {new_line}"
                    elif child.attribute == 'DO':
                        # Если следующий дочерний элемент имеет атрибут "DO", выводим его на той же строке
                        new_line = self._format_tree(child, 0)
                        result[-1] += f" {new_line}"
                    else:
                        # Остальные дочерние элементы выводятся с новой строки и увеличенным уровнем отступа
                        if child.attribute in ['END_IF', 'END_FOR', 'END_WHILE', 'END_FUNC', 'END_PROC',
                                               'END_ITERATOR']:
                            # Закрывающие узлы выравниваются с открывающими
                            new_lines = self._format_tree(child, level)
                            result.append(new_lines)
                        else:
                            # Остальные дочерние элементы выводятся с увеличенной табуляцией
                            new_lines = self._format_tree(child, level + 1)
                            result.append(new_lines)
                else:
                    # Для других нетерминалов просто добавляем отступ
                    if child.attribute in ['END_IF', 'END_FOR', 'END_WHILE', 'END_FUNC', 'END_PROC', 'END_ITERATOR']:
                        # Закрывающие узлы выравниваются с открывающими
                        new_lines = self._format_tree(child, level)
                        result.append(new_lines)
                    else:
                        # Остальные дочерние элементы выводятся с увеличенной табуляцией
                        new_lines = self._format_tree(child, level + 1)
                        result.append(new_lines)

        return '\n'.join(result)

    def add_line_numbers(self, text, start_line=1):
        """
        Добавляет нумерацию строк, начиная со второй строки.
        :param text: Исходный текст.
        :param start_line: Номер первой строки для нумерации.
        :return: Текст с нумерацией строк.
        """
        lines = text.split('\n')
        result = []

        for i, line in enumerate(lines):
            if i == 0:
                # Первая строка остается без изменений
                result.append(line)
            else:
                # Нумерация начинается со второй строки
                result.append(f"{start_line + i - 1}: {line}")

        return '\n'.join(result)

class Publisher:
    def __init__(self, text):
        self.text = text

    def to_latex(self, text):
        """
        Преобразует отформатированный текст в LaTeX с использованием пакета listings.
        :param text: Исходный текст.
        :return: Текст в формате LaTeX (только содержимое lstlisting).
        """
        lines = text.split('\n')
        latex_result = []

        # Добавляем строки текста
        for line in lines:
            latex_result.append(line)

        return '\n'.join(latex_result)

    def convert_ansi_to_latex(self, text):
        """
        Преобразует ANSI escape-коды в LaTeX-команды.
        :param text: Исходный текст с ANSI-цветами.
        :return: Текст с LaTeX-цветами.
        """
        # Словарь соответствия ANSI-цветов и LaTeX-цветов
        color_mapping = {
            '\033[91m': '\\textcolor{red}{',  # Красный
            '\033[94m': '\\textcolor{blue}{',  # Синий
            '\033[0m': '}'  # Сброс цвета
        }

        # Заменяем ANSI-коды на LaTeX-команды
        for ansi_code, latex_command in color_mapping.items():
            text = text.replace(ansi_code, latex_command)

        return text

    def save_to_latex(self, text, filename="output.tex"):
        """
        Сохраняет отформатированный текст в файл LaTeX.
        :param text: Исходный текст.
        :param filename: Имя файла для сохранения.
        """
        # Преобразуем ANSI-коды в LaTeX-команды
        text = self.convert_ansi_to_latex(text)

        # Создаем полный LaTeX-документ
        latex_document = r"""
    \documentclass{article}
    \usepackage{xcolor} % Для работы с цветами
    \usepackage{fancyvrb} % Для вывода текста с цветами

    \begin{document}
    \begin{Verbatim}[commandchars=\\\{\}]
    """ + text + r"""
    \end{Verbatim}
    \end{document}
    """

        # Сохраняем в файл
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(latex_document)

        print(f"LaTeX file saved as {filename}")

# Класс для раскраски текста
class Highlighter:
    def __init__(self, color_rules):
        self.color_rules = color_rules

    def highlight(self, text):
        highlighted_text = text
        for token, color in self.color_rules.items():
            pattern = re.compile(r'\b' + re.escape(token) + r'\b')
            highlighted_text = pattern.sub(self._apply_color(token, color), highlighted_text)

        # Дополнительно раскрашиваем терминалы в красный
        highlighted_text = self._highlight_terminals(highlighted_text)
        return highlighted_text

    def _apply_color(self, text, color):
        # ANSI escape codes for colors
        colors = {
            'red': '\033[91m',
            'blue': '\033[94m',
            'reset': '\033[0m'
        }
        return f"{colors[color]}{text}{colors['reset']}"

    def _highlight_terminals(self, text):
        # Ищем терминалы в тексте (например, значения или атрибуты)
        lines = text.split('\n')
        for i in range(len(lines)):
            # Пропускаем корневой узел "Program"
            if lines[i].strip().startswith('Program'):
                continue
            # Если строка содержит терминал (не начинается с ключевого слова)
            if not any(keyword in lines[i] for keyword in self.color_rules.keys()):
                # Окрашиваем всю строку в красный цвет
                lines[i] = self._apply_color(lines[i], 'red')
        return '\n'.join(lines)


# Подклассы для Publisher
class LinePublisher(Publisher):
    def convert_ansi_to_latex(self, text):
        color_mapping = {
            '\033[91m': r'|\textcolor{red}{',  # Красный
            '\033[94m': r'|\textcolor{blue}{',  # Синий
            '\033[0m': r'}|'  # Сброс цвета
        }

        for ansi_code, latex_command in color_mapping.items():
            text = text.replace(ansi_code, latex_command)

        # Экранируем символы `_`
        text = text.replace('_', r'\_')

        return text

    def save_to_latex(self, text, filename="output.tex"):
        text = self.convert_ansi_to_latex(text)

        latex_document = r"""
    \documentclass{article}
    \usepackage{xcolor} % Для работы с цветами
    \usepackage{listings} % Для вывода текста с цветами и переносами
    \usepackage{geometry} % Для настройки полей
    \geometry{a4paper, left=10mm, right=10mm, top=10mm, bottom=10mm} % Минимальные поля

    % Настройка listings для переноса строк и раскраски
    \lstset{
        basicstyle=\ttfamily\footnotesize, % Моноширинный шрифт
        breaklines=true, % Разрешить перенос строк
        postbreak=\mbox{\textcolor{red}{$\hookrightarrow$}\space}, % Символ переноса
        columns=fullflexible, % Гибкие колонки
        frame=none, % Без рамки
        xleftmargin=0pt, % Нет отступа слева
        xrightmargin=0pt, % Нет отступа справа
        showstringspaces=false, % Не показывать пробелы в строках
        escapeinside=||, % Позволяет вставлять LaTeX-коды внутри листинга
    }

    \begin{document}
    \begin{lstlisting}
    """ + text + r"""
    \end{lstlisting}
    \end{document}
    """

        # Сохраняем в файл
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(latex_document)

        print(f"LaTeX file saved as {filename}")


class LadderPublisher(Publisher):
    pass


class TreePublisher(Publisher):
    pass


# Подклассы для Highlighter
class LineHighlighter(Highlighter):
    pass


class LadderHighlighter(Highlighter):
    pass


class TreeHighlighter(Highlighter):
    def _highlight_terminals(self, text):
        """
        Раскрашивает терминалы в красный цвет, исключая символы |--.
        """
        lines = text.split('\n')
        for i in range(len(lines)):
            if lines[i].strip().startswith('Program'):
                continue
            if not any(keyword in lines[i] for keyword in self.color_rules.keys()):
                # Разделяем строку на части, чтобы не окрашивать |--
                parts = lines[i].split('|--')
                # Окрашиваем только терминалы (после |--)
                if len(parts) > 1:
                    parts[1] = self._apply_color(parts[1], 'red')
                    lines[i] = '|--'.join(parts)
        return '\n'.join(lines)


def create_publisher(style, text):
    if style == 'line':
        return LinePublisher(text)
    elif style == 'ladder':
        return LadderPublisher(text)
    elif style == 'tree':
        return TreePublisher(text)
    else:
        raise ValueError("Unsupported style")


def create_highlighter(style, color_rules):
    if style == 'line':
        return LineHighlighter(color_rules)
    elif style == 'ladder':
        return LadderHighlighter(color_rules)
    elif style == 'tree':
        return TreeHighlighter(color_rules)
    else:
        raise ValueError("Unsupported style")


if __name__ == "__main__":
    # Создаем пример AST для сортировки пузырьком
    ast = TreeNode(
        node_type=NodeType.NONTERMINAL,
        nonterminal_type='Program',
        children=[
            TreeNode(
                node_type=NodeType.NONTERMINAL,
                nonterminal_type='FOR',
                children=[
                    TreeNode(node_type=NodeType.TERMINAL, attribute='Loop', value='i FROM 0 TO n - 1'),
                    TreeNode(node_type=NodeType.TERMINAL, attribute='DO', value='DO'),
                    TreeNode(
                        node_type=NodeType.NONTERMINAL,
                        nonterminal_type='FOR',
                        children=[
                            TreeNode(node_type=NodeType.TERMINAL, attribute='Loop', value='j FROM 0 TO n - i - 2'),
                            TreeNode(node_type=NodeType.TERMINAL, attribute='DO', value='DO'),
                            TreeNode(
                                node_type=NodeType.NONTERMINAL,
                                nonterminal_type='IF',
                                children=[
                                    TreeNode(node_type=NodeType.TERMINAL, attribute='Condition', value='arr[j] > arr[j + 1]'),
                                    TreeNode(node_type=NodeType.TERMINAL, attribute='THEN', value='THEN'),
                                    TreeNode(node_type=NodeType.TERMINAL, attribute='Action', value='SWAP(arr[j], arr[j + 1])'),
                                    TreeNode(node_type=NodeType.TERMINAL, attribute='END_IF', value='END_IF')
                                ]
                            ),
                            TreeNode(node_type=NodeType.TERMINAL, attribute='END_FOR', value='END_FOR')
                        ]
                    ),
                    TreeNode(node_type=NodeType.TERMINAL, attribute='END_FOR', value='END_FOR')
                ]
            )
        ]
    )

    # Определяем правила раскраски для ключевых слов
    KEYWORDS = [
        'IF', 'THEN', 'ELSE', 'ELSEIF', 'END_IF',
        'FOR', 'DO', 'END_FOR', 'REPEAT', 'UNTIL',
        'WHILE', 'END_WHILE', 'FUNC', 'END_FUNC',
        'PROC', 'END_PROC', 'ITERATOR', 'END_ITERATOR',
        'INPUT', 'OUTPUT', 'GOTO', 'ARRAY', 'STRUCT',
        'SELECT', 'YIELD', 'RETURN', 'NEXT', 'FROM', 'TO', 'IN'
    ]

    # Создаем правила раскраски: ключевые слова красятся в синий
    color_rules = {keyword: 'blue' for keyword in KEYWORDS}

    # Форматируем и раскрашиваем
    style = 'tree'  # line/ladder/tree
    formatter = Formatter(style=style)
    highlighter = create_highlighter(style, color_rules)

    # Извлекаем только текст из результата format
    formatted_text = formatter.format(ast)
    highlighted_text = highlighter.highlight(formatted_text)
    numbered_text = formatter.add_line_numbers(highlighted_text)

    publisher = create_publisher(style, numbered_text)
    print("Highlighted Text:")
    print(numbered_text, "\n")

    publisher.save_to_latex(numbered_text, filename="bubble_sort.tex")
