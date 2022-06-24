def parse_type(value: int | float | str, cast_type: str) -> bool | float | int:
    try:
        if cast_type == 'bool':
            if value == 'true':
                return True
            if value == 'false':
                return False
            if isinstance(value, bool):
                return bool(value)
            return False if float(value) == 0.0 else True
        if cast_type == 'int':
            return int(value)
        if cast_type == 'real':
            return float(value)
    except ValueError:
        fail_interpreter('помилка парсингу', (value, cast_type))


# def parse_str(value: int | float | str, cast_type: str) -> bool | float | int:
#     if cast_type == 'bool':
#         return bool(value)
#         return False if value == 0 else True
#     if cast_type == 'int':
#         return int(float(value))
#     if cast_type == 'real':
#         return float(value)


def compare_value(lex: str, value_l: str, value_r) -> bool:
    if lex == '<=':
        return True if value_l <= value_r else False
    if lex == '==':
        return True if value_l == value_r else False
    if lex == '>=':
        return True if value_l >= value_r else False
    if lex == '<':
        return True if value_l < value_r else False
    if lex == '>':
        return True if value_l > value_r else False
    if lex == '!=':
        return True if value_l != value_r else False
    if lex == 'or':
        return True if value_l or value_r else False
    if lex == 'and':
        return True if value_l and value_r else False


def fail_interpreter(error: str, data: tuple):
    if error == 'неініціалізована змінна':
        (lx, (lexeme_l, token_l), lex, (lexeme_r, token_r)) = data
        print('POLIS ERROR: неініціалізована змінна')
        raise SystemExit(
            'Значення змінної {0} не визначене.\nЗустрілось у {1} {2} {3}\nКод помилки: {4}'
                .format(lx, (lexeme_l, token_l), lex, (lexeme_r, token_r), 301))
    if error == 'ділення на нуль':
        ((lexeme_l, token_l), lex, (lexeme_r, token_r)) = data
        print('POLIS ERROR: ділення на нуль')
        raise SystemExit(
            'Ділення на нуль у {0} {1} {2}.\nКод помилки: {3}'
                .format((lexeme_l, token_l), lex, (lexeme_r, token_r), 302))
    if error == 'немає вказаної мітки':
        print('POLIS ERROR: відсутня вказана мітка')
        raise SystemExit(
            'У коді програми немає мітки {0}.\nСтрибок не можливий.\nКод помилки: {1}'
                .format(data, 303))
    if error == 'помилка парсингу':
        print('POLIS ERROR: помилка парсингу')
        value, cast_type = data
        raise SystemExit(
            'Не можливо привести значення {0} до типу {1}.\nКод помилки: {2}'
                .format(value, cast_type, 304))
    # if error = ''

def get_value_token(value: int | float | bool) -> str:
    if isinstance(value, bool):
        return 'bool'
    if isinstance(value, int):
        return 'int'
    if isinstance(value, float):
        return 'real'


def get_lexeme(token: str, value: int | bool | float) -> str:
    if token == 'bool':
        return 'true' if value is True else 'false'
    else:
        return str(value)
