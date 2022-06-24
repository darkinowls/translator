from lab5.polis.BasicPolisAnalyser import BasicPolisAnalyser
from lab5.polis.polis_helper import fail_interpreter, parse_type


class AdvancedPolisAnalyser(BasicPolisAnalyser):

    def interpret_operation(self, lex, tok, index: int) -> int:

        if tok == 'jump':
            return self.get_jump_index(lex, tok, index)
        if tok == 'jump_if':
            return self.get_jump_if_index(lex, tok)
        if tok == 'io':
            self.do_io_idents(lex)
            return index
        return super().interpret_operation(lex, tok, index)

    def get_jump_index(self, lex, tok, index) -> int:
        lexeme_r, token_r = self.stack.pop()
        value_r = self.get_ident_or_const_value(lexeme_r, token_r, lex, lex, tok)
        if not value_r:
            return index
        try:
            return self.postfix_code.index((lex, 'mark')) + 1
        except ValueError:
            fail_interpreter('немає вказаної мітки', (lex, 'mark'))

    def get_jump_if_index(self, lex, tok):
        lexeme_r, token_r = self.stack.pop()
        value_r = self.get_ident_or_const_value(lexeme_r, token_r, lex, lex, tok)
        try:
            if value_r:
                return self.postfix_code.index((lex, 'mark_true')) + 1
            return self.postfix_code.index((lex, 'mark_false')) + 1
        except ValueError:
            fail_interpreter('немає вказаної мітки', (lex, 'mark'))

    def do_io_idents(self, lex):
        if lex == 'read':
            self.read_idents()
            return
        if lex == 'write':
            self.write_idents()
            return

    def read_idents(self):
        lexeme_r, token_r = self.stack.pop()
        print('Read:')
        while True:
            self.get_ident_or_const_value(lexeme_r, 'ident', 'read', 'read()', 'io'  )
            value = input('{0} = '.format(lexeme_r))
            self.id_table[lexeme_r] = (
                self.id_table[lexeme_r][0], self.id_table[lexeme_r][1], parse_type(value, self.id_table[lexeme_r][1]))
            lexeme_r, token_r = self.stack.pop()
            if token_r != 'ident_list':
                return

    def write_idents(self):
        lexeme_r, token_r = self.stack.pop()
        print('Write:')
        while True:
            self.get_ident_or_const_value(lexeme_r, 'ident', 'write', 'write()', 'io')
            print('{0} = {1}'.format(lexeme_r, self.id_table[lexeme_r][2]))
            lexeme_r, token_r = self.stack.pop()
            if token_r != 'ident_list':
                return
