from lab5.polis.AdvancedPolisAnalyser import AdvancedPolisAnalyser
from lab5.syntax.SyntaxAnalyser import SyntaxAnalyser
from lex_manager import analyse_lex, read_file
from lab5.polis.BasicPolisAnalyser import BasicPolisAnalyser

if __name__ == "__main__":

    correct, message, symbol_table, id_table, const_table = analyse_lex(
        read_file('E:/university/3kurs2sem/Translators/Lab5/test.base'))
    print('-' * 40)
    print('SYMBOL_TABLE:{0}'.format(symbol_table))
    print('ID_TABLE:{0}'.format(id_table))
    print('CONST_TABLE:{0}'.format(const_table))

    syntax_analyser = SyntaxAnalyser(symbol_table, id_table)
    syntax_analyser.parse_program()
    # print(syntax_analyser.message)

    print('-' * 100)
    print('SYMBOL_TABLE:{0}'.format(symbol_table))
    print('ID_TABLE:{0}'.format(id_table))
    print('CONST_TABLE:{0}'.format(const_table))
    print(syntax_analyser.postfix_code)
    print()

    polis_analyser = AdvancedPolisAnalyser(syntax_analyser.postfix_code, id_table, const_table)
    polis_analyser.polis_interpret()
    print('\nID_TABLE:')
    for key in id_table:
        print('{0} : {1}'.format(key, id_table[key]))

    print('MARKS:' , syntax_analyser.mark_table)
