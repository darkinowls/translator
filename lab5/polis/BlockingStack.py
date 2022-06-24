class BlockingStack:
    items: list[tuple]

    def __init__(self):
        self.items = []

    def is_empty(self) -> bool:
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self) -> tuple:
        if not self.is_empty():
            return self.items.pop()
        return False, False

    def print(self):
        sx = ""
        for x in self.items:
            sx += str(x) + '\t'
        print('STACK:[ {0} '.format(sx))
        return True
