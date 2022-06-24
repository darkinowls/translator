from consts import ABC, TOKENS, STATES_TRANSITIONS, FINAL, END_TYPES

LEXER = 'Lexer'


def get_char(source_code: str, index: int) -> tuple[chr, int]:
    try:
        char = source_code[index]
    except IndexError:
        char = '!'  # To invoke end
    index += 1
    return char, index


def analyse_lex(source_code: str) -> tuple[bool, str, list, dict, dict]:
    message: str = ''
    symbol_table: list = []
    id_table: dict = {}
    const_table: dict = {}
    state: int = 0
    lexeme: str = ''
    char: chr = ''
    line_num: int = 1
    index: int = 0
    try:
        while index <= len(source_code):
            char, index = get_char(source_code, index)
            char_class = get_char_class(char, state)
            state = get_next_state(state, char_class)
            if is_final(state):
                line_num, lexeme, index, message = process_lexeme(state,
                                                                  line_num,
                                                                  lexeme,
                                                                  char,
                                                                  index,
                                                                  symbol_table,
                                                                  id_table,
                                                                  const_table,
                                                                  message)
                state = 0
            elif state == 0:
                lexeme = ''
            else:
                lexeme += char
    except SystemExit as e:
        print(message)
        print(symbol_table)
        print(id_table)
        print(const_table)
        raise SystemExit('{0}\n{1}: Аварійне завершення програми з кодом {2}'
            .format(
            exit_with_fail(state, line_num, char),
            LEXER,
            e))

    return True, message + '\n{0}: Лексичний аналіз завершено успішно'.format(
        LEXER), symbol_table, id_table, const_table


def read_file(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()


def get_char_class(char: chr, state: int) -> str:
    if state == 5 and char == 'E':
        return char
    if char in '.':
        return "dot"
    if char in " \t":
        return "ws"
    if char == "\n":
        return "nl"
    if char in "+-=*/^();:<>,!":
        return char
    for k, v in ABC.items():
        if char in k:
            return v
    return 'символ не належить алфавіту'


def get_next_state(state: int, char_class: str) -> int:
    try:
        return STATES_TRANSITIONS[(state, char_class)]
    except KeyError:
        return STATES_TRANSITIONS[(state, 'other')]


def is_final(state: int) -> bool:
    return True if state in FINAL else False


def process_lexeme(state: int, line_num: int, lexeme: str, char: chr, index: int,
                   symbol_table: list, id_table: dict, const_table: dict, message: str) -> tuple[int, str, int, str]:
    if state == 8:  # \n
        return line_num + 1, lexeme, index, message
    elif state in END_TYPES.keys() or state in (14, 15):
        token = get_token_or_type(state, lexeme)
        number = get_number_from_table(state, lexeme, token, id_table, const_table) if token not in (
            'keyword', 'compare_op', 'logic_op') else ''
        message += '\n{0:<3d} {1:<20s} {2:<10s} {3:>3s} '.format(line_num, lexeme, token, str(number))
        symbol_table.append((line_num, lexeme, token, number))
        return line_num, '', index - 1, message
    elif state == 7:
        lexeme += char
        token = get_token_or_type(state, char)
        message += '\n{0:<3d} {1:<20s} {2:<10s} '.format(line_num, lexeme, token)
        symbol_table.append((line_num, lexeme, token, ''))
        return line_num, '', index, message
    exit(state)


def exit_with_fail(state: int, line_num: int, char: chr) -> str:
    if state == 101:
        return '\n{0}: у рядку {1} неочікуваний символ {2}'.format(LEXER, line_num, char)
    elif state == 102:
        return '\n{0}: у рядку {1} неочікуваний символ {2} після експоненти E'.format(LEXER, line_num, char)


def get_token_or_type(state: int, lexeme: str) -> str:
    for k, v in TOKENS.items():
        if lexeme in k:
            return v
    return END_TYPES[state]


def get_number_from_table(state: int, lexeme: str, token: str, id_table: dict, const_table: dict) -> int:
    number = None
    id_data = None
    value: float | int | bool = 0
    if state == 2 and token != 'bool':
        id_data = id_table.get(lexeme)
        if id_data is None:
            number = len(id_table) + 1
            id_table[lexeme] = (number, 'type_undef', 'val_undef')
    elif state in (6, 9) or token == 'bool':
        id_data = const_table.get(lexeme)
        if id_data is None:
            number = len(const_table) + 1
            if state == 6:
                value = float(lexeme)
            elif state == 9:
                value = int(lexeme)
            elif token == 'bool':
                value = True if lexeme == 'true' else False
            const_table[lexeme] = (number, token, value)
    if id_data is not None:
        if len(id_data) == 2:
            number, _ = id_data
        else:
            number, _, _ = id_data
    return number
