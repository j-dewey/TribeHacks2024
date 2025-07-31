class StringTree:
    def __init__(self, strings: list[str]) -> None:
        self.head = StringTreeNode('')
        for st in strings:
            self.head.push_str(st)
    
    def predict_string(self, string: str) -> str:
        return self.head.predict_from_string(string)

class StringTreeNode:
    def __init__(self, val) -> None:
        self.val = val
        self.letters = {}
    
    def push_str(self, string: str):
        if len(string) == 0: return
        if string[0] in self.letters.keys():
            self.letters[string[0]].push_str(string[1::])
            return 
        node = StringTreeNode(string[0])
        node.push_str(string[1::])
        self.letters[string[0]] = node
    
    def make_random_word(self) -> str:
        if len(self.letters.keys()) == 0: return ''
        letter = next(iter(self.letters))
        return letter + self.letters[letter].make_random_word()

    def predict_from_string(self, string: str) -> str:
        if string != '':
            if not string[0] in self.letters.keys():
                return ''
            return string[0] + self.letters[string[0]].predict_from_string(string[1::])
        if len(self.letters.keys()) == 0: 
            return ''
        letter = next(iter(self.letters.keys())) # cannot index into it
        return letter + self.letters[letter].predict_from_string(string)