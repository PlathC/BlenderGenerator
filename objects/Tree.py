class Branch:
    def __init__(self,parent):
        self.__parent = parent

class Rule:

    def __init__(self,_from,_to):
        self.__from = _from
        self.__to = _to

    def apply(self,char):
        res = char
        if char == self.__from:
            res = self.__to
        return res


class Tree:

    def __parseChar(self, char, p):
        nextP = [0,0,0]
        if char == 'F':
            nextP = [0,0,0]
        elif char == '[':
            nextP = [0, 0, 0]
        elif char == ']':
            nextP = [0, 0, 0]
        elif char == '+':
            nextP = [0, 0, 0]
        elif char == '-':
            nextP = [0, 0, 0]
        return nextP

    def __next_step(self):
        new_word = ""
        for char in self.__word:
            new_sequence =  char
            for rule in self.__rules:
                rule_sequence = rule.apply(char)
                if rule_sequence != char:
                    new_sequence = rule_sequence
            new_word = new_word + new_sequence

        self.__word = new_word

    def __init__(self):
        """

        """
        self.__points = []
        self.__word = "F"
        self.__rules = []

        self.__rules.append(Rule('F', 'FF+[+F-F-F]-[-F+F+F]'))

        for i in range(1, 3):
            self.__next_step()

        print(self.__word)
        p = [0, 0, 0]
        for c in self.__word:
            self.__points.append(self.__parseChar(c, p))

        print(self.__points)
