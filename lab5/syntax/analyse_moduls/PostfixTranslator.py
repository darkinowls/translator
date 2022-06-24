from collections import deque


class PostfixTranslator:
    postfix_code: list[tuple[str, str]]

    def __init__(self, infix_code: list = list()):
        self.postfix_code = infix_code

    def add_to_postfix(self, element: tuple[str, str]):
        self.postfix_code.append(element)
