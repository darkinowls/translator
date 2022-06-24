from lab5.consts import ANY, SYNTAXER
from lab5.syntax.analyse_moduls.AdvancedSyntaxAnalyser import AdvancedSyntaxAnalyser


class SyntaxAnalyser(AdvancedSyntaxAnalyser):
    def __init__(self, symbol_table: list, id_table: dict):
        super().__init__(symbol_table, id_table)

    def parse_program(self) -> tuple[bool, str]:
        try:
            self.parse_token('program', 'keyword')
            self.parse_token(ANY, 'ident')
            self.parse_decl_section()
            self.parse_do_section()
            return True, self.message + '\n{0}: Синтаксичний аналіз завершився успішно'.format(SYNTAXER)
        except SystemExit as error:
            print(self.message)
            raise SystemExit('{0}: Аварійне завершення програми з кодом {1}'.format(SYNTAXER, error))
