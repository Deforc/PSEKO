import yaml


class Formatter:

    KEYWORDS = [
        'IF', 'THEN', 'ELSE', 'ELSEIF', 'END_IF',
        'FOR', 'DO', 'END_FOR', 'REPEAT', 'UNTIL',
        'WHILE', 'END_WHILE', 'FUNC', 'END_FUNC',
        'PROC', 'END_PROC', 'ITERATOR', 'END_ITERATOR',
        'INPUT', 'OUTPUT', 'GOTO', 'ARRAY', 'STRUCT',
        'SELECT', 'YIELD', 'RETURN', 'NEXT', 'FROM', 'TO', 'IN'
    ]

    def __init__(self, file_path, format_type, keyword_color, comment_color):
        self.file_path = file_path
        self.format_type = format_type
        self.end_terminals = ['ELSE', 'END_IF', 'END_WHILE', 'END_FOR']
        self.keyword_color = keyword_color
        self.comment_color = comment_color

    def _colorize(self, text, keyword_color):
        """Add ANSI color codes to text"""
        return f"\\textcolor [HTML]{keyword_color}{text}"


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
                result_text += self._colorize(node['value'], self.comment_color) + ' '
            else:
                # Обрабатываем ключевые слова
                value = self._colorize(node['value'], self.keyword_color) if node['value'] in self.KEYWORDS else node[
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
        result_text += 'Program'
        if (self.format_type == 'string'):
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
        """Конвертирует отформатированный текст в LaTeX"""
        lines = text.split('\n')
        latex_lines = []

        # Удаляем первую строку с "Program"
        if lines and lines[0].strip() == 'Program':
            lines = lines[1:]

        for line in lines:
            if not line.strip():
                continue

            # Определяем уровень отступа
            current_indent = len(line) - len(line.lstrip())
            indent_level = current_indent // 4

            # Удаляем ANSI коды цветов
            clean_line = self._remove_ansi_codes(line.strip())

            # Обработка комментариев
            if clean_line.startswith('//'):
                comment = clean_line[2:].strip()
                latex_lines.append('    ' * indent_level + f'\\STATE \\textcolor [HTML]{color_comment}{comment}')
                continue

            # Разбиваем строку на токены
            tokens = clean_line.split()
            if not tokens:
                continue

            # Обработка конструкций
            if tokens[0] == 'FOR':
                condition = ' '.join(t for t in tokens[1:] if t != 'DO')
                latex_lines.append('    ' * indent_level + f'\\FOR{{{condition}}}')
                indent_level += 1
            elif tokens[0] == 'IF':
                condition = ' '.join(t for t in tokens[1:] if t != 'THEN')
                latex_lines.append('    ' * indent_level + f'\\IF{{{condition}}}')
                indent_level += 1
            elif tokens[0] == 'WHILE':
                condition = ' '.join(t for t in tokens[1:] if t != 'DO')
                latex_lines.append('    ' * indent_level + f'\\WHILE{{{condition}}}')
                indent_level += 1
            elif tokens[0] in ['END_IF', 'END_FOR', 'END_WHILE']:
                indent_level -= 1
                latex_lines.append('    ' * indent_level + f'\\{tokens[0].replace("END_", "END")}')
            elif tokens[0] == 'NEXT':
                latex_lines.append('    ' * indent_level + '\\BREAK')
            elif tokens[0] == 'RETURN':
                value = ' '.join(tokens[1:]) if len(tokens) > 1 else ''
                latex_lines.append('    ' * indent_level + f'\\RETURN {value}')
            else:
                # Обычное выражение
                expr = ' '.join(tokens)
                latex_lines.append('    ' * indent_level + f'\\STATE {expr}')

        # Собираем полный LaTeX документ
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
\\caption{{Program}}
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
# formatter = Formatter('example8.yaml', 'ladder')
# print(formatter.get_formatted())
# latex_code = formatter.export_to_latex()
# print(latex_code)
