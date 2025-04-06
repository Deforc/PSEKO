import yaml

class Formatter:
    def __init__(self, file_path, format_type):
        self.file_path = file_path
        self.format_type = format_type
        self.end_terminals = ['ELSE', 'END_IF', 'END_WHILE', 'END_FOR']
        #self.tree: str = self._deserializeAST()

    def _read_ast(self) -> dict:
        with open(self.file_path, 'r', encoding="utf-8") as stream:
            data_loaded = yaml.safe_load(stream)
        return data_loaded

    def _process_nonterminal(self, node: dict, blocks_before: int) -> str:
        result_text: str = ''

        if (node['value'] == ''):
            if (node['subtype'] == 'Block'):
                result_text += self._process_block(node, blocks_before)
            else:
                for child in node['children']:
                        result_text += self._process_nonterminal(child, blocks_before)
        else:
            if (node['value'] in self.end_terminals):
                    result_text += '\n' + '\t' * blocks_before
            result_text += node['value'] + ' '
            for child in node['children']:
                result_text += self._process_nonterminal(child, blocks_before)

        return result_text

    def _process_block(self, node: dict, blocks_before: int) -> str:
        result_text: str = ''
        if (node['subtype'] == 'Block'):
            result_text += '\n' + '\t' * (blocks_before + 1)
            #result_text += '---'
            for child in node['children']:
                result_text += self._process_nonterminal(child, blocks_before + 1)

        return result_text

    def _process_programm(self, node: dict) -> str:
        result_text: str = ''
        blocks_before: int = 0;
        assert node['subtype'] == 'Program'
        #if (node['subtype'] == 'Program'):
        result_text += 'Program'
            #print(result_text)
        
        for child in node['children']:
            result_text += self._process_block(child, blocks_before)
        return result_text

    def _deserialize_ast(self) -> str:
        ast = self._read_ast()
        return self._process_programm(ast)
    
    def get_formatted(self) -> str:
        ast = self._deserialize_ast()
        return ast
    
#a = Formatter('ast_after.yaml', 'ladder')
a = Formatter('example8.yaml', 'ladder')
ast = a.get_formatted()
print(ast)