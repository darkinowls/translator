from lab5.polis.BlockingStack import BlockingStack
from lab5.polis.polis_helper import fail_interpreter, compare_value, parse_type, \
    get_value_token, get_lexeme
from lab5.syntax.analyse_moduls.PostfixTranslator import PostfixTranslator


class BasicPolisAnalyser(PostfixTranslator):
    stack: BlockingStack
    id_table: dict
    const_table: dict

    def __init__(self, infix_code: list, id_table: dict, const_table: dict):
        super().__init__(infix_code)
        self.stack = BlockingStack()
        self.id_table = id_table
        self.const_table = const_table

    def polis_interpret(self):
        step: int = 0
        index: int = 0
        while index < len(self.postfix_code):
            taken_lexeme, taken_token = self.postfix_code[index]
            if taken_token.startswith('mark'):
                index += 1
                continue
            if taken_token in ('int', 'real', 'ident', 'bool', 'ident_list'):
                self.stack.push((taken_lexeme, taken_token))
                index += 1
                step += 1
            else:
                index = self.interpret_operation(taken_lexeme, taken_token, index + 1)
                step += 1
            # self.print_interpret(step, taken_lexeme, taken_token)

    def interpret_operation(self, lex, tok, index: int) -> int:
        (lexeme_r, token_r) = self.stack.pop()
        if tok in ('not_op', 'unary_minus'):
            value_r = self.get_ident_or_const_value(lexeme_r, token_r, lex, tok, tok)
            self.calculate_unary(lex, (value_r, lexeme_r, token_r))
            return index
        (lexeme_l, token_l) = self.stack.pop()
        if (lex, tok) == ('=', 'assign_op'):
            self.get_ident_or_const_value(lexeme_l, token_l, lex, lexeme_r, token_r)
            value_r = self.get_ident_or_const_value(lexeme_r, token_r, lex, lexeme_l, token_l)
            self.id_table[lexeme_l] = \
                (self.id_table[lexeme_l][0],
                 self.id_table[lexeme_l][1],
                 parse_type(value_r, self.id_table[lexeme_l][1]))
            return index
        if tok in ('add_op', 'mult_op', 'pow_op', 'compare_op', 'logic_op'):
            id_elem_l, lex, id_elem_r = self.get_values((lexeme_l, token_l), lex, (lexeme_r, token_r))
            self.calculate_binary(id_elem_l, lex, id_elem_r)
            return index
        return index

    def get_values(self, left_tuple: tuple, lex: str, right_tuple: tuple) -> tuple[tuple, str, tuple]:
        lexeme_l, token_l = left_tuple
        lexeme_r, token_r = right_tuple
        value_l = self.get_ident_or_const_value(lexeme_l, token_l, lex, lexeme_r, token_r)
        value_r = self.get_ident_or_const_value(lexeme_r, token_r, lex, lexeme_l, token_l)
        return (value_l, lexeme_l, token_l), lex, (value_r, lexeme_r, token_r)

    def get_ident_or_const_value(self, lexeme_l, token_l, lex, lexeme_r, token_r) -> int | bool | float | None:
        if token_l == 'ident':
            if lexeme_l not in self.id_table or self.id_table[lexeme_l][1] == 'type_undef':
                fail_interpreter('неініціалізована змінна',
                                 (lexeme_l, (lexeme_l, token_l), lex,
                                  (lexeme_r, token_r)))
            return self.id_table[lexeme_l][2]
        return self.const_table[lexeme_l][2]


    def calculate_binary(self, id_elem_l: tuple, lex: str, id_elem_r: tuple):
        value_l, lexeme_l, token_l = id_elem_l
        value_r, lexeme_r, token_r = id_elem_r
        value: bool | int | float = 0
        if lex == '+':
            value = value_l + value_r
        elif lex == '-':
            value = value_l - value_r
        elif lex == '*':
            value = value_l * value_r
        elif lex == '/' and value_r == 0:
            fail_interpreter('ділення на нуль', ((lexeme_l, token_l), lex, (lexeme_r, token_r)))
        elif lex == '/':
            value = value_l / value_r
        elif lex == '^':
            value = value_l ** value_r
        elif lex in ('<=', '==', '>=', '<', '>', '!=', 'or', 'and'):
            value = compare_value(lex, value_l, value_r)
        token = get_value_token(value)
        lexeme = get_lexeme(token, value)
        self.stack.push((lexeme, token))
        self.add_to_const_table(lexeme, value, token)

    def calculate_unary(self, lex: str, id_elem_r: tuple):
        value_r, lexeme_r, token_r = id_elem_r
        if lex == '&':
            value = -value_r
        elif lex == '!':
            value = True if value_r == 0 else False
        token = get_value_token(value)
        lexeme = get_lexeme(token, value)
        self.stack.push((lexeme, token))
        self.add_to_const_table(lexeme, value, token)

    def add_to_const_table(self, lexeme: int | str | float, value: int | bool | float, token):
        id_data = self.const_table.get(lexeme)
        if id_data is None:
            number = len(self.const_table) + 1
            self.const_table[lexeme] = (number, token, value)

    def print_interpret(self, step: int, lex: str, tok: str):
        if step == 1:
            print('=' * 30 + '\nInterpreter run\n')
            print(self.id_table)
            print(self.const_table)
        print('\nКрок інтерпретації: {0}'.format(step))
        if lex == 'end_expression':
            print('Завершення виразу')
        elif tok in ('int', 'real', 'bool'):
            print('Лексема: {0} у таблиці констант: {1}'.format((lex, tok), lex + ':' + str(self.const_table[lex])))
        elif tok == 'ident':
            print('Лексема: {0} у таблиці ідентифікаторів: {1}'.format((lex, tok), lex + ':' + str(self.id_table[lex])))
        else:
            print('Лексема: {0}'.format((lex, tok)))
        print('postfixCode={0}'.format(self.postfix_code))
        self.stack.print()
