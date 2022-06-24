from lab5.consts import TAB, NL, ANY, SYNTAXER, TYPES
from lab5.syntax.analyse_moduls.BasicSyntaxAnalyser import BasicSyntaxAnalyser


class DeclarationAnalyser(BasicSyntaxAnalyser):
    id_table: dict

    def __init__(self, symbol_table: list, id_table: dict):
        super().__init__(symbol_table)
        self.id_table = id_table

    def parse_ident_list(self, tabs: int = 0) -> list[str]:
        self.message += NL + TAB * tabs + 'parse_ident_list():'
        idents: list = []
        while True:
            line_number, taken_lexeme, taken_token, _ = self.get_symbol()
            if not self.parse_token(ANY, 'ident', tabs + 1):
                return idents
            idents.append(taken_lexeme)
            line_number, taken_lexeme, taken_token, _ = self.get_symbol()
            if (taken_lexeme, taken_token) != (',', 'coma'):
                return idents
            self.message += NL + '{0}{1}: В рядку {2} токен {3}'.format(TAB * (tabs + 1), SYNTAXER, line_number,
                                                                        (taken_lexeme, taken_token))
            self.row_number += 1

    def parse_decl(self, tabs: int = 0) -> bool:
        self.message += NL + TAB * tabs + 'parse_decl():'
        idents = self.parse_ident_list(tabs + 1)
        self.parse_token(':', 'colon', tabs + 1)
        line_number, taken_lexeme, taken_token, _ = self.get_symbol()
        if taken_lexeme not in TYPES:
            self.fail_parsing(204, (line_number, taken_lexeme, taken_token, TYPES))
        self.message += NL + '{0}{1}: В рядку {2} токен {3}'.format(TAB * (tabs + 1), SYNTAXER, line_number,
                                                                    (taken_lexeme, taken_token))
        self.set_idents_value(idents, taken_lexeme)
        self.row_number += 1
        return True

    def parse_decl_list(self, tabs: int = 0):
        self.message += NL + tabs * TAB + 'parse_decl_list():'
        while True:
            self.parse_decl(tabs + 1)
            line_number, taken_lexeme, taken_token, _ = self.get_symbol()
            if (taken_lexeme, taken_token) != (';', 'end_colon'):
                return
            self.message += NL + '{0}{1}: В рядку {2} токен {3}'.format(TAB * (tabs + 1), SYNTAXER, line_number,
                                                                        (taken_lexeme, taken_token))
            self.row_number += 1

    def parse_decl_section(self, tabs: int = 0):
        self.message += NL + tabs * TAB + 'parse_decl_section():'
        self.parse_token('var', 'keyword', tabs + 1)
        self.parse_decl_list(tabs + 1)

    def set_idents_value(self, idents: list[str], str_type: str):
        value: float | bool | int = 0
        for ident in idents:
            if str_type == 'real':
                value = 0.0
            elif str_type == 'bool':
                value = False
            self.id_table[ident] = (self.id_table[ident][0], str_type, value)
