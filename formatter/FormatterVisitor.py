from models.TreeNode import TreeNode, NodeType  # Импортируем TreeNode и NodeType
from utils.Visitor import Visitor  # Импортируем базовый Visitor

class FormatterVisitor(Visitor):
    def __init__(self, style="лесенка"):
        self.style = style
        self.indent_level = 0
        self.indent_size = 4

    def indent(self):
        """Возвращает строку с отступом."""
        return " " * (self.indent_level * self.indent_size)

    def visit_program(self, node: TreeNode):
        """Форматирование для Program."""
        result = []
        for child in node.childs:
            result.append(child.accept(self))
        return "\n".join(result)

    def visit_block(self, node: TreeNode):
        """Форматирование для Block."""
        self.indent_level += 1
        result = [f"{self.indent()}{{\n"]
        for child in node.childs:
            result.append(child.accept(self))
        result.append(f"{self.indent()}}}\n")
        self.indent_level -= 1
        return "".join(result)

    def visit_assignment(self, node: TreeNode):
        """Форматирование для Assignment."""
        variable = node.childs[0].accept(self)
        expression = node.childs[1].accept(self)
        return f"{self.indent()}{variable} : {expression}\n"

    def visit_conditional(self, node: TreeNode):
        """Форматирование для Conditional."""
        condition = node.childs[0].accept(self)
        then_block = node.childs[1].accept(self)
        result = [f"{self.indent()}IF {condition} THEN\n{then_block}"]
        if len(node.childs) > 2:  # Есть ELSEIF или ELSE
            for child in node.childs[2:]:
                result.append(child.accept(self))
        result.append(f"{self.indent()}END_IF\n")
        return "".join(result)


# Аналогично для других узлов (Loop, FunctionDecl и т.д.)