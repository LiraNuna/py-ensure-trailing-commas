import ast, asttokens


class MissingTrailingCommaFinder(ast.NodeVisitor):
    def __init__(self, atok):
        self.atok = atok
        self.insertion_indexes = set()

    def until_token_forward(self, token, until):
        while token.string != until:
            token = self.atok.next_token(token, include_extra=True)

        return token

    def until_token_backwards(self, token, until):
        while token.string != until:
            token = self.atok.prev_token(token, include_extra=True)

        return token

    def find_trailing_commas(self, start_token, end_token):
        tokens = list(self.atok.token_range(start_token, end_token, include_extra=True))
        first_token, *rest, last_token = tokens

        start_line, start_column = first_token.start
        end_line, end_column = last_token.end
        if start_line == end_line:
            return

        *rest, should_be_newline = rest
        if should_be_newline.string != '\n':
            return

        *rest, should_be_comma = rest
        if should_be_comma.string == ',':
            return

        self.insertion_indexes.add(should_be_comma.endpos)

    def visit_Call(self, node):
        super().generic_visit(node)

        if not node.args and not node.keywords:
            return

        self.find_trailing_commas(node.first_token, node.last_token)

    def visit_Tuple(self, node):
        super().generic_visit(node)

        if not node.elts:
            return

        self.find_trailing_commas(
            self.until_token_backwards(node.first_token, '('),
            self.until_token_forward(node.last_token, ')'),
        )

    def visit_List(self, node):
        super().generic_visit(node)

        if not node.elts:
            return

        self.find_trailing_commas(node.first_token, node.last_token)

    def visit_Dict(self, node):
        super().generic_visit(node)

        if not node.keys or not node.values:
            return

        self.find_trailing_commas(node.first_token, node.last_token)

    def visit_FunctionDef(self, node):
        super().generic_visit(node)

        argument_list = node.args.args
        if not argument_list:
            return

        self.find_trailing_commas(
            self.until_token_backwards(argument_list[0].first_token, '('),
            self.until_token_forward(argument_list[-1].last_token, ')'),
        )

    def visit_ClassDef(self, node):
        super().generic_visit(node)

        bases_list = node.bases
        if not node.bases:
            return

        self.find_trailing_commas(
            self.until_token_backwards(bases_list[0].first_token, '('),
            self.until_token_forward(bases_list[-1].last_token, ')'),
        )


with open('util.py') as file:
    file_contents = file.read()

    atok = asttokens.ASTTokens(file_contents, parse=True)
    comma_finder = MissingTrailingCommaFinder(atok)
    comma_finder.visit(atok.tree)

    for index in sorted(comma_finder.insertion_indexes, reverse=True):
        file_contents = file_contents[:index] + ',' + file_contents[index:]

    print(file_contents)
