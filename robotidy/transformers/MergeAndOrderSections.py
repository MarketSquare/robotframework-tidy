from robot.api.parsing import (
    Token,
    ModelTransformer,
    SectionHeader,
    EmptyLine
)
from robot.parsing.model.blocks import Section
from robot.parsing.model.statements import Statement


class MergeAndOrderSections(ModelTransformer):
    def __init__(self):
        self.sections_order = (
            Token.COMMENT_HEADER,
            Token.SETTING_HEADER,
            Token.VARIABLE_HEADER,
            Token.TESTCASE_HEADER,
            Token.KEYWORD_HEADER
        )

    def visit_File(self, node):
        if len(node.sections) < 2:
            return node
        sections = {}
        last = len(node.sections) - 1
        for index, section in enumerate(node.sections):
            if index == last:
                section = self.from_last_section(section)
            section_type, body, header = self.get_section_data(section)
            if section_type not in sections:
                sections[section_type] = {
                    'body': body,
                    'header': header
                }
            else:
                if len(header.data_tokens) > 1:
                    print(f'{node.source}: Merged duplicated section has section header comments. '
                          'Only header comments from first section header of the same type are preserved.')
                sections[section_type]['body'] += body
        node.sections = []
        for order in self.sections_order:
            if order not in sections:
                continue
            node.sections.append(Section(header=sections[order]['header'], body=sections[order]['body']))
        return node

    @staticmethod
    def from_last_section(node):
        """ Last node use different logic for new line marker. It is not possible to preserve all empty lines but
        we need at least ensure that following code::

             *** Test Case ***
             *** Variables ***

        Will not become::
            *** Variables ****** Test Case ***

        """
        if node.body:
            last_statement = node.body[-1]
            new_line = [Token(Token.EOL, '\n')]
            if hasattr(last_statement, 'body'):
                if not last_statement.body:
                    node.body[-1].body.append(EmptyLine.from_params(eol='\n'))
                else:
                    last_statement = last_statement.body[-1]
                    if hasattr(last_statement, 'end'):
                        if last_statement.end:
                            node.body[-1].body[-1].end = Statement.from_tokens(
                                list(last_statement.end.tokens[:-1]) + new_line
                            )
                    else:
                        node.body[-1].body[-1] = Statement.from_tokens(list(last_statement.tokens[:-1]) + new_line)
            else:
                node.body[-1] = Statement.from_tokens(list(last_statement.tokens[:-1]) + new_line)
        else:
            last_token = node.header.tokens[-1]
            if last_token.type == Token.EOL:
                node.header = Statement.from_tokens(list(node.header.tokens[:-1]) + [Token(Token.EOL, '\n')])
        return node

    @staticmethod
    def get_section_data(section):
        header_tokens = (Token.COMMENT_HEADER, Token.TESTCASE_HEADER, Token.SETTING_HEADER, Token.KEYWORD_HEADER,
                         Token.VARIABLE_HEADER)
        if section.header:
            name_token = section.header.get_token(*header_tokens)
            section_type = name_token.type
            header = section.header
        else:
            section_type = Token.COMMENT_HEADER
            header = SectionHeader.from_params(section_type, '*** Comments ***')
        return section_type, section.body, header
