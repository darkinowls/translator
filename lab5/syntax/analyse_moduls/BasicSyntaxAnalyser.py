from lab5.consts import TAB, NL, ANY, SYNTAXER, END_TYPES
from lab5.syntax.analyse_moduls.PostfixTranslator import PostfixTranslator


class BasicSyntaxAnalyser(PostfixTranslator):
    symbol_table: list
    row_number: int
    message: str

    def __init__(self, symbol_table):
        super().__init__()
        self.symbol_table = symbol_table
        self.row_number = 0
        self.message = ''

    def parse_token(self, lexeme: tuple | str, token: tuple | str, tabs: int = 0) -> bool:
        if self.row_number > len(self.symbol_table):
            self.fail_parsing(201, (lexeme, token, self.row_number))
        line_number, taken_lexeme, taken_token, _ = self.get_symbol()
        self.row_number += 1
        if ((taken_lexeme in lexeme) or (lexeme == ANY)) and taken_token in token:
            self.message += NL + '{0}{1}: В рядку {2} токен {3}'.format(tabs * TAB, SYNTAXER, line_number,
                                                                        (taken_lexeme, taken_token))
            return True
        self.fail_parsing(203, (line_number, taken_lexeme, taken_token, lexeme, token))

    def get_symbol(self) -> tuple[int, str, str, int]:
        try:
            return self.symbol_table[self.row_number]
        except IndexError:
            self.fail_parsing(202, self.row_number)

    def fail_parsing(self, error: int, data: tuple | int) -> None:
        if error == 201:
            (lexeme, token, self.row_number) = data
            self.message += NL + '{0} ERROR: \n\t Неочікуваний кінець програми ' \
                                 '- в таблиці символів (розбору) немає запису з номером {1}. \n\t Очікувалось - {2}' \
                .format(SYNTAXER, self.row_number, (lexeme, token))
            raise SystemExit(201)
        if error == 202:
            (self.row_number) = data
            self.message += NL + '{0} ERROR: \n\t Неочікуваний кінець програми ' \
                                 '- в таблиці символів (розбору) немає запису з номером {1}. \n\t Останній запис - {2}' \
                .format(SYNTAXER, self.row_number, self.symbol_table[self.row_number - 1])
            raise SystemExit(202)
        if error == 203:
            (line_number, lexeme, token, taken_lexeme, taken_token) = data
            self.message += NL + '{0} ERROR: \n\t В рядку {1} неочікуваний елемент ({2},{3}). \n\t Очікувався - ({4},{5}).' \
                .format(SYNTAXER, line_number, lexeme, token, taken_lexeme, taken_token)
            raise SystemExit(203)
        if error == 204:
            (line_number, taken_lexeme, taken_token, expected) = data
            self.message += NL + '{0} ERROR: \n\t В рядку {1} неочікуваний елемент ({2},{3}). \n\t Очікувався - {4}.' \
                .format(SYNTAXER, line_number, taken_lexeme, taken_token, expected)
            raise SystemExit(204)
        if error == 205:
            (line_number, lexeme) = data
            self.message += NL + '{0} ERROR: \n\t В рядку {1} зустрічається використана мітка {2}.' \
                .format(SYNTAXER, line_number, lexeme)
            raise SystemExit(205)
        if error == 206:
            lexeme, line_num = data
            self.message = NL + '{0} ERROR: \n\t Змінна {1} не є міткою. Помилка в рядку {2}' \
                .format(SYNTAXER, lexeme, line_num)
            raise SystemExit(206)

    def parse_add(self, tabs: int) -> str:
        line_number, taken_lexeme, taken_token, _ = self.get_symbol()
        if taken_token == 'add_op':
            self.message += NL + TAB * tabs + 'parse_add():'
            self.parse_token(taken_lexeme, taken_token, tabs + 1)
            if taken_lexeme == '-':
                return '&'
        return ''

    def parse_arithm_expression(self, tabs: int = 0):
        self.message += NL + TAB * tabs + 'parse_arithm_expression():'
        unary_minus = self.parse_add(tabs + 1)
        self.parse_term(tabs + 1)
        while True:
            line_number, taken_lexeme, taken_token, _ = self.get_symbol()
            if taken_token != 'add_op':
                if unary_minus == '&':
                    self.postfix_code.append((unary_minus, 'unary_minus'))
                return
            self.row_number += 1
            self.message += NL + TAB * (tabs + 1) + 'в рядку {0} - {1}'.format(line_number, (taken_lexeme, taken_token))
            self.parse_term(tabs + 1)
            self.add_to_postfix((taken_lexeme, taken_token))

    def parse_term(self, tabs: int = 0):
        self.message += NL + TAB * tabs + 'parse_term():'
        self.parse_factor(tabs + 1)
        while True:
            line_number, taken_lexeme, taken_token, _ = self.get_symbol()
            if taken_token != 'mult_op':
                return
            self.row_number += 1
            self.message += NL + TAB * (tabs + 1) + 'в рядку {0} - {1}'.format(line_number, (taken_lexeme, taken_token))
            self.parse_factor(tabs + 1)
            self.add_to_postfix((taken_lexeme, taken_token))

    def parse_factor(self, tabs: int = 0):
        self.message += NL + TAB * tabs + 'parse_factor():'
        pow_counter = 0
        self.parse_element(tabs + 1)
        while True:
            line_number, taken_lexeme, taken_token, _ = self.get_symbol()
            if taken_token != 'pow_op':
                [self.add_to_postfix(('^', 'pow_op')) for i in range(pow_counter)]
                return
            self.row_number += 1
            self.message += NL + TAB * (tabs + 1) + 'в рядку {0} - {1}'.format(line_number, (taken_lexeme, taken_token))
            self.parse_element(tabs + 1)
            pow_counter += 1

    def parse_element(self, tabs: int = 0):
        line_number, taken_lexeme, taken_token, _ = self.get_symbol()
        self.message += NL + TAB * tabs + 'parse_element(): рядок: {0} (lex, tok):{1}' \
            .format(line_number, (taken_lexeme, taken_token))
        if taken_token in END_TYPES.values() or taken_token == 'bool':
            self.row_number += 1
            self.message += NL + TAB * (tabs + 1) + 'в рядку {0} - {1}'.format(line_number, (taken_lexeme, taken_token))
            self.add_to_postfix((taken_lexeme, taken_token))
        elif taken_lexeme == '(':
            self.message += NL + TAB * tabs + 'в рядку {0} - {1}'.format(line_number, (taken_lexeme, taken_token))
            self.row_number += 1
            self.parse_expression(tabs + 1)
            self.parse_token(')', 'par_op', tabs + 1)
        else:
            self.fail_parsing(204,
                              (line_number, taken_lexeme, taken_token,
                               'bool, int, real, ident або \'(\' Expression \')\''))

    def parse_not(self, tabs: int = 0) -> bool:
        line_number, taken_lexeme, taken_token, _ = self.get_symbol()
        if (taken_lexeme, taken_token) == ('!', 'not_op'):
            self.message += NL + TAB * tabs + 'parse_not():'
            self.parse_token(taken_lexeme, taken_token, tabs + 1)
            return True
        return False

    def parse_expression(self, tabs: int = 0):
        self.message += NL + TAB * tabs + 'parse_expression():'
        is_not = self.parse_not(tabs + 1)
        self.parse_arithm_expression(tabs + 1)
        while True:
            line_number, taken_lexeme, taken_token, _ = self.get_symbol()
            if taken_token not in ('compare_op', 'logic_op'):
                if is_not:
                    self.postfix_code.append(('!', 'not_op'))
                return
            self.row_number += 1
            self.message += NL + TAB * (tabs + 1) + 'в рядку {0} - {1}'.format(line_number, (taken_lexeme, taken_token))
            self.parse_arithm_expression(tabs + 1)
            self.add_to_postfix((taken_lexeme, taken_token))
