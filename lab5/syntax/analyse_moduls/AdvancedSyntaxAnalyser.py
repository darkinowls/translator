from lab5.consts import TAB, NL, ANY
from lab5.polis.polis_helper import fail_interpreter
from lab5.syntax.analyse_moduls.DeclarationAnalyser import DeclarationAnalyser


class AdvancedSyntaxAnalyser(DeclarationAnalyser):
    mark_table: dict
    for_mark_num: int

    def __init__(self, symbol_table, id_table):
        super().__init__(symbol_table, id_table)
        self.mark_table = dict()
        self.for_mark_num = 0

    def parse_for(self, tabs: int = 0):
        self.message += NL + TAB * tabs + 'parse_for():'
        for_mark_num = self.for_mark_num
        self.for_mark_num += 1
        self.parse_token('for', 'keyword', tabs + 1)
        self.parse_ind_expr(for_mark_num, tabs + 1)
        self.add_to_postfix(('loop{0}'.format(for_mark_num), 'mark_true'))
        self.parse_do_section(tabs + 1)
        self.add_to_postfix(('true', 'bool'))
        self.add_to_postfix(('step{0}'.format(for_mark_num), 'jump'))
        self.add_to_postfix(('loop{0}'.format(for_mark_num), 'mark_false'))
        return True

    def parse_ind_expr(self, for_mark_num: int, tabs: int = 0, ):
        self.message += NL + TAB * tabs + 'parse_ind_expr():'
        self.parse_token('(', 'par_op', tabs + 1)
        _, taken_lexeme, taken_token, _ = self.get_symbol()
        self.parse_assign(tabs + 1)
        self.parse_token(';', 'end_colon', tabs + 1)
        self.add_to_postfix(('check{0}'.format(for_mark_num), 'mark'))
        self.parse_expression(tabs + 1)
        self.add_to_postfix(('loop{0}'.format(for_mark_num), 'jump_if'))
        self.parse_token(';', 'end_colon', tabs + 1)
        self.add_to_postfix(('step{0}'.format(for_mark_num), 'mark'))
        self.add_to_postfix((taken_lexeme, taken_token))
        self.parse_expression(tabs + 1)
        self.add_to_postfix(('=', 'assign_op'))
        self.add_to_postfix(('true', 'bool'))
        self.add_to_postfix(('check{0}'.format(for_mark_num), 'jump'))
        self.parse_token(')', 'par_op', tabs + 1)

    def parse_assign(self, tabs: int = 0) -> bool:
        self.message += NL + TAB * tabs + 'parse_assign():'
        line_number, taken_lexeme, taken_token, _ = self.get_symbol()
        self.row_number += 1
        self.message += NL + TAB * (tabs + 1) + 'в рядку {0} - {1}'.format(line_number, (taken_lexeme, taken_token))
        self.add_to_postfix((taken_lexeme, taken_token))
        if self.parse_token('=', 'assign_op', tabs + 1):
            self.parse_expression(tabs + 1)
            self.add_to_postfix(('=', 'assign_op'))
            return True
        return False

    def parse_io(self, tabs: int = 0) -> bool:
        self.message += NL + TAB * tabs + 'parse_io():'
        line_number, taken_lexeme, taken_token, _ = self.get_symbol()
        self.parse_token(('read', 'write'), 'keyword', tabs + 1)
        self.parse_token('(', 'par_op', tabs + 1)
        idents = self.parse_ident_list(tabs + 1)
        self.parse_token(')', 'par_op', tabs + 1)
        [self.add_to_postfix((ident, 'ident_list')) for ident in idents]
        self.add_to_postfix((taken_lexeme, 'io'))
        return True

    def parse_statement(self, tabs: int = 0) -> bool:
        self.message += NL + TAB * tabs + 'parse_statement():'
        self.parse_mark(tabs + 1)
        line_number, taken_lexeme, taken_token, _ = self.get_symbol()
        if taken_lexeme in ('read', 'write'):
            return self.parse_io(tabs + 1)
        if taken_token == 'ident':
            return self.parse_assign(tabs + 1)
        if (taken_lexeme, taken_token) == ('if', 'keyword'):
            return self.parse_if(tabs + 1)
        if (taken_lexeme, taken_token) == ('for', 'keyword'):
            return self.parse_for(tabs + 1)
        self.fail_parsing(204, (line_number, taken_lexeme, taken_token, 'ident або if або for або io'))

    def parse_statement_list(self, tabs: int = 0):
        self.message += NL + TAB * tabs + 'parse_statement_list():'
        while True:
            self.parse_statement(tabs + 1)
            line_number, taken_lexeme, taken_token, _ = self.get_symbol()
            if (taken_lexeme, taken_token) == ('end', 'keyword'):
                return
            self.parse_token(';', 'end_colon', tabs + 1)

    def parse_do_section(self, tabs: int = 0):
        self.message += NL + TAB * tabs + 'parse_do_section():'
        self.parse_token('begin', 'keyword', tabs + 1)
        self.parse_statement_list(tabs + 1)
        self.parse_token('end', 'keyword', tabs + 1)

    def parse_if(self, tabs: int = 0) -> bool:
        self.message += NL + TAB * tabs + 'parse_if():'
        self.row_number += 1
        self.parse_expression(tabs + 1)
        self.parse_token('then', 'keyword', tabs + 1)
        self.parse_token('goto', 'keyword', tabs + 1)
        line_number, taken_lexeme, taken_token, _ = self.get_symbol()
        self.parse_token(taken_lexeme, 'ident', tabs + 1)
        self.add_to_postfix((taken_lexeme, 'jump'))
        return True

    def parse_mark(self, tabs: int = 0):
        line_number, taken_lexeme, taken_token, _ = self.get_symbol()
        if taken_token == 'ident':
            self.row_number += 1
            line_number_2, taken_lexeme_2, taken_token_2, _ = self.get_symbol()
            if (taken_lexeme_2, taken_token_2) == (':', 'colon'):
                self.row_number += 1
                self.message += NL + TAB * tabs + 'parse_mark():'
                self.message += NL + TAB * (tabs + 1) + 'в рядку {0} - {1}'.format(line_number,
                                                                                   (taken_lexeme, taken_token))
                self.message += NL + TAB * (tabs + 1) + 'в рядку {0} - {1}'.format(line_number_2,
                                                                                   (taken_lexeme_2, taken_token_2))
                self.make_label(line_number, taken_lexeme)
                return
            self.row_number -= 1

    def make_label(self, line_number: int, lexeme: str):
        if lexeme not in self.id_table:
            self.fail_parsing(205, (line_number, lexeme))
        if 'type_undef' != self.id_table.pop(lexeme)[1]:
            self.fail_parsing(206, (lexeme, line_number) )
        self.mark_table[lexeme] = line_number
        self.add_to_postfix((lexeme, 'mark'))
