TOKENS = {('program', 'var', 'begin', 'end', 'if', 'for', 'then',
           'goto', 'read', 'write', 'int', 'real', 'bool'): 'keyword',
          ('-', '+'): 'add_op',
          ('true', 'false'): 'bool',
          ('or', 'and'): 'logic_op',
          '=': 'assign_op',
          ',': 'coma',
          '.': 'dot',
          ';': 'end_colon',
          ':': 'colon',
          '!': 'not_op',
          ('<=', '==', '>=', '<', '>', '!='): 'compare_op',
          (' ', '\t'): 'ws',
          ('*', '/'): 'mult_op',
          ('(', ')'): 'par_op',
          '^': 'pow_op'}

END_TYPES = {2: 'ident', 6: 'real', 9: 'int'}

TYPES = ('real', 'int', 'bool')

ABC = {
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ': 'Letter',
    "0123456789": 'Digit'
}

OPERATIONS = ['hidden_assign', 'io']

STATES_TRANSITIONS = {(0, 'Letter'): 1, (1, 'Letter'): 1, (1, 'Digit'): 1, (1, 'other'): 2,
                      (0, 'Digit'): 4, (4, 'Digit'): 4, (4, 'other'): 9,
                      (4, 'dot'): 5, (5, 'Digit'): 5, (5, 'E'): 10, (5, 'other'): 6,
                      (10, '+'): 17, (10, '-'): 17,
                      (17, 'Digit'): 16, (17, 'other'): 102,
                      (10, 'Digit'): 16, (10, 'other'): 102,
                      (16, 'Digit'): 16, (16, 'other'): 6,
                      (0, 'ws'): 0,
                      (0, 'nl'): 8,
                      (0, '+'): 7, (0, '-'): 7, (0, '*'): 7, (0, '/'): 7, (0, '('): 7, (0, ';'): 7,
                      (0, ')'): 7, (0, '='): 7, (0, '^'): 7, (0, ','): 7, (0, ':'): 7,
                      (0, 'other'): 101,
                      (0, '<'): 12, (0, '='): 12, (0, '>'): 12, (0, '!'): 12,
                      (12, 'other'): 14, (12, '='): 13,
                      (13, 'other'): 15,
                      }

FINAL = {2, 6, 9, 7, 8, 14, 15, 101, 102}
F_ERROR = {101, 102}

SYNTAXER: str = 'Syntaxer'
TAB: str = '\t'
NL: str = '\n'
ANY: str = '%ANY%'
