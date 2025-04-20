import yaml


class Formatter:

    KEYWORDS = [
        'IF', 'THEN', 'ELSE', 'ELSEIF', 'END_IF',
        'FOR', 'DO', 'END_FOR', 'REPEAT', 'UNTIL',
        'WHILE', 'END_WHILE', 'FUNC', 'END_FUNC',
        'PROC', 'END_PROC', 'ITERATOR', 'END_ITERATOR',
        'INPUT', 'OUTPUT', 'GOTO', 'ARRAY', 'STRUCT',
        'SELECT', 'YIELD', 'RETURN', 'NEXT', 'FROM', 'TO', 'IN', 'OF', 'CALL'
    ]

    def __init__(self, file_path, format_type, keyword_color, comment_color):
        self.file_path = file_path
        self.format_type = format_type
        self.end_terminals = ['ELSE', 'END_IF', 'END_WHILE', 'END_FOR', 'END_FUNC', 'END_PROC', 'UNTIL']
        self.keyword_color = keyword_color
        self.comment_color = comment_color

    def _colorize(self, text):
        """Add ANSI color codes to text"""
        return f"\\textcolor [HTML]{{{self.keyword_color}}}{{{text}}}"


    def _read_ast(self) -> dict:
        with open(self.file_path, 'r', encoding="utf-8") as stream:
            data_loaded = yaml.safe_load(stream)
        return data_loaded

    def _process_nonterminal(self, node: dict, blocks_before: int) -> str:
        result_text: str = ''

        if node['value'] == '':
            if node['subtype'] == 'Block':
                result_text += self._process_block(node, blocks_before)
            else:
                # Обработка комментариев на уровне NONTERMINAL
                if node.get('subtype') == 'Comment':
                    for child in node['children']:
                        if child.get('subtype') == 'commenttext':
                            result_text += f"\\textcolor [HTML]{{{self.comment_color}}}{{{child['value']}}} "
                else:
                    if (node['subtype'] == 'FieldDecl'):
                        result_text += '\n' + '\t' * blocks_before
                    for child in node['children']:
                        result_text += self._process_nonterminal(child, blocks_before)
        else:
            # Сохраняем оригинальную логику переносов для всех узлов
            if node['value'] in self.end_terminals:
                if self.format_type == 'ladder':
                    result_text += '\n' + '\t' * blocks_before
                elif self.format_type == 'string':
                    result_text += ' '
                elif self.format_type == 'tree':
                    result_text += '\n' + '\t' * blocks_before + '|-- '

            # Обрабатываем комментарии (добавляем без дополнительных переносов)
            if node.get('subtype') == 'commenttext':
                result_text += f"\\textcolor [HTML]{{{self.comment_color}}}{{{node['value']}}} "
            else:
                # Обрабатываем ключевые слова
                value = self._colorize(node['value'].replace('_', '\\_')) if node['value'] in self.KEYWORDS else node[
                    'value']
                result_text += value + ' '

            # Рекурсивно обрабатываем дочерние элементы
            for child in node['children']:
                result_text += self._process_nonterminal(child, blocks_before)

        return result_text

    def _process_block(self, node: dict, blocks_before: int) -> str:
        result_text: str = ''
        if (node['subtype'] == 'Block'):
            if (self.format_type == 'ladder'):
                result_text += '\n' + '\t' * (blocks_before + 1)
            elif (self.format_type == 'string'):
                result_text += ''
            elif (self.format_type == 'tree'):
                result_text += '\n' + '\t' * (blocks_before + 1) + '|-- '
            for child in node['children']:
                result_text += self._process_nonterminal(child, blocks_before + 1)

        return result_text

    def _process_programm(self, node: dict) -> str:
        result_text: str = ''
        blocks_before: int = 0
        assert node['subtype'] == 'Program'

        # Не добавляем имя программы в результат для string формата
        if self.format_type != 'string':
            result_text += f'{node["children"][0]["value"]}'
            if self.format_type == 'string':
                result_text += ' '

        for child in node['children']:
            result_text += self._process_block(child, blocks_before)
        return result_text

    def _deserialize_ast(self) -> str:
        ast = self._read_ast()
        return self._process_programm(ast)

    def get_formatted(self) -> str:
        ast = self._deserialize_ast()
        return ast

    def export_to_latex(self, output_file: str = None) -> str:
        """
        Экспорт в LaTeX на основе уже отформатированного текста
        :param output_file: если None, возвращает строку, иначе сохраняет в файл
        :return: LaTeX-код или None если сохранено в файл
        """
        formatted_text = self.get_formatted()
        color_comment = self.comment_color
        latex_code = self._convert_to_latex(formatted_text, color_comment)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(latex_code)
            return None
        return latex_code

    def _convert_to_latex(self, text: str, color_comment: str) -> str:
        ast = self._read_ast()
        program_name = ast.get('attribute', 'Program')
        lines = text.split('\n')
        latex_lines = []
        indent_stack = [0]  # Стек для отслеживания уровней вложенности

        # Удаляем первую строку с именем программы, если она есть
        if lines and lines[0].strip() == program_name:
            lines = lines[1:]

        for line in lines:
            if not line.strip():
                continue

            # Определяем текущий уровень отступа
            current_indent = len(line) - len(line.lstrip('\t'))

            # Корректируем стек отступов
            if current_indent > indent_stack[-1]:
                indent_stack.append(current_indent)
            elif current_indent < indent_stack[-1]:
                while indent_stack and current_indent < indent_stack[-1]:
                    indent_stack.pop()
                if not indent_stack:
                    indent_stack.append(0)

            indent_level = len(indent_stack) - 1
            clean_line = self._remove_ansi_codes(line.strip())

            # Обработка комментариев
            if clean_line.startswith('//'):
                comment = clean_line[2:].strip()
                latex_lines.append(f'\\STATE \\textcolor[HTML]{{{color_comment}}}{{{comment}}}')
                continue

            tokens = clean_line.split()
            if not tokens:
                continue

            # Обработка конструкций
            if tokens[0] == 'WHILE':
                condition = ' '.join(tokens[1:-1])  # Убираем DO
                latex_line = f'\\STATE \\textcolor[HTML]{{{self.keyword_color}}}{{WHILE}} {condition} \\textcolor[HTML]{{{self.keyword_color}}}{{DO}}'
            elif tokens[0] == 'IF':
                condition = ' '.join(tokens[1:-1])  # Убираем THEN
                latex_line = f'\\STATE \\textcolor[HTML]{{{self.keyword_color}}}{{IF}} {condition} \\textcolor[HTML]{{{self.keyword_color}}}{{THEN}}'
            elif tokens[0] == 'END_WHILE':
                latex_line = f'\\STATE \\textcolor[HTML]{{{self.keyword_color}}}{{END\\_WHILE}}'
            elif tokens[0] == 'END_IF':
                latex_line = f'\\STATE \\textcolor[HTML]{{{self.keyword_color}}}{{END\\_IF}}'
            elif tokens[0] == 'RETURN':
                value = ' '.join(tokens[1:]) if len(tokens) > 1 else ''
                latex_line = f'\\STATE \\textcolor[HTML]{{{self.keyword_color}}}{{RETURN}} {value}'
            elif tokens[0] == 'END_FUNC':
                latex_line = f'\\STATE \\textcolor[HTML]{{{self.keyword_color}}}{{END\\_FUNC}}'
            elif tokens[0] == 'END_PROC':
                latex_line = f'\\STATE \\textcolor[HTML]{{{self.keyword_color}}}{{END\\_PROC}}'
            elif tokens[0] == 'UNTIL':
                condition = ' '.join(tokens[1:])
                latex_line = f'\\STATE \\textcolor[HTML]{{{self.keyword_color}}}{{UNTIL}} {condition}'
            else:
                # Обычные строки
                latex_line = f'\\STATE {" ".join(tokens)}'

            # Добавляем отступ
            if indent_level > 0:
                indent_space = '\\hspace{%dmm}' % (indent_level * 8)
                latex_line = latex_line.replace('\\STATE', f'\\STATE {indent_space}', 1)
            else:
                latex_line = latex_line.replace('\\STATE', '\\STATE \\hspace{0mm}', 1)

            latex_lines.append(latex_line)

        body = '\n'.join(latex_lines)
        return f"""\\documentclass{{article}}
    \\usepackage[utf8]{{inputenc}}
    \\usepackage[english,russian]{{babel}}
    \\usepackage{{algorithm}}
    \\usepackage{{algorithmic}}
    \\usepackage{{xcolor}}
    \\usepackage{{amsmath}}

    \\begin{{document}}

    \\begin{{algorithm}}
    \\caption{{{program_name}}}
    \\begin{{algorithmic}}[1]
    {body}
    \\end{{algorithmic}}
    \end{{algorithm}}

    \end{{document}}"""

    def _remove_ansi_codes(self, text: str) -> str:
        """Удаляет ANSI коды цветов из текста"""
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)


# Использование с цветами по умолчанию (ключевые слова - синие, комментарии - зеленые)
formatter = Formatter('example21.yaml', format_type='ladder', keyword_color='0000FF', comment_color='008000')
# print(formatter.get_formatted())
latex_code = formatter.export_to_latex()
print(latex_code)
