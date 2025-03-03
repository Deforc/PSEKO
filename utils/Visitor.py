from models.TreeNode import TreeNode, NodeType
from core.ast import AST


class Visitor:
    def visit(self, node: TreeNode):
        """Метод для посещения узла."""
        if node.type == NodeType.NONTERMINAL:
            return self.visit_nonterminal(node)
        elif node.type == NodeType.TERMINAL:
            return self.visit_terminal(node)
        else:
            raise ValueError(f"Unknown node type: {node.type}")

    def visit_nonterminal(self, node: TreeNode):
        """Метод для посещения нетерминального узла."""
        method_name = f"visit_{node.nonterminal_type.lower()}"
        if hasattr(self, method_name):
            return getattr(self, method_name)(node)
        else:
            return self.default_visit(node)

    def visit_terminal(self, node: TreeNode):
        """Метод для посещения терминального узла."""
        return self.default_visit(node)

    def default_visit(self, node: TreeNode):
        """Метод по умолчанию для узлов, которые не обрабатываются явно."""
        result = []
        for child in node.childs:
            result.append(child.accept(self))
        return "".join(result)
