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
        self.end_terminals = ['ELSE', 'END_IF', 'END_WHILE', 'END_FOR', 'UNTIL', 'END_FUNC', 'END_PROC']
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
                result_text += self._colorize(node['value']) + ' '
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
        # result_text += f'{node["children"][0]["value"]}'
        self.caption = node["children"][0]["value"]
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
        print(formatted_text)
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
            indent_level = current_indent // 2

            # Удаляем ANSI коды цветов
            clean_line = self._remove_ansi_codes(line.strip())
            # Добавляем отступы
            indent = '\\hspace{' + str(indent_level * 4) + 'mm}'
            # Обработка комментариев
            if clean_line.startswith('//'):
                comment = clean_line[2:].strip()
                latex_lines.append('    ' * indent_level + f'\\STATE \\textcolor [HTML]{{{color_comment}}}{{{comment}}}')
                continue

            # Разбиваем строку на токены
            tokens = clean_line.split()
            if not tokens:
                continue

            # Обработка конструкций
            if tokens[0] == 'IF':
                condition = ' '.join(t for t in tokens[1:] if t != 'THEN')
                latex_lines.append(
                    f'\\STATE {indent} \\textcolor [HTML]{{0000FF}}{{IF}} {condition} \\textcolor [HTML]{{0000FF}}{{THEN}}')
            elif tokens[0] == 'ELSE':
                latex_lines.append(f'\\STATE {indent} \\textcolor [HTML]{{0000FF}}{{ELSE}}')
            elif tokens[0] == 'END_IF':
                latex_lines.append(f'\\STATE {indent} \\textcolor [HTML]{{0000FF}}{{END\_IF}}')
            elif tokens[0] == 'FOR':
                condition = ' '.join(t for t in tokens[1:] if t != 'DO')
                latex_lines.append(
                    f'\\STATE {indent} \\textcolor [HTML]{{0000FF}}{{FOR}} {condition} \\textcolor [HTML]{{0000FF}}{{DO}}')
            elif tokens[0] == 'END_FOR':
                latex_lines.append(f'\\STATE {indent} \\textcolor [HTML]{{0000FF}}{{END\_FOR}}')
            elif tokens[0] == 'WHILE':
                condition = ' '.join(t for t in tokens[1:] if t != 'DO')
                latex_lines.append(
                    f'\\STATE {indent} \\textcolor [HTML]{{0000FF}}{{WHILE}} {condition} \\textcolor [HTML]{{0000FF}}{{DO}}')
            elif tokens[0] == 'END_WHILE':
                latex_lines.append(f'\\STATE {indent} \\textcolor [HTML]{{0000FF}}{{END\_WHILE}}')
            else:
                # Обычное выражение
                expr = ' '.join(tokens)
                latex_lines.append(f'\\STATE {indent} {expr}')

        # Собираем полный LaTeX документ

        body = '\n'.join(latex_lines)
        print(body)
        return f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[english,russian]{{babel}}
\\usepackage{{algorithm}}
\\usepackage{{algorithmic}}
\\usepackage{{xcolor}}
\\usepackage{{amsmath}}

\\begin{{document}}

\\begin{{algorithm}}
\\caption{{{self.caption}}}
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
# formatter = Formatter('example2.yaml', 'ladder',)
# print(formatter.get_formatted())
# latex_code = formatter.export_to_latex()
# print(latex_code)
