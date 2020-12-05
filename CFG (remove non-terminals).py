class CFG:
    def __init__(self, **args):
        self.terminals = args['terminals']
        self.nonterminals = args['nonterminals']
        self.start = args['start']
        self.rules = args['rules']
        self.remove_e()
        self.remove_nongenerative_nonterminals()
        self.remove_unreachable_nonterminals()

    def remove_e(self):
       keys = list(self.rules.keys())
       for k in keys:
            for el in self.rules[k]:
                if el == 'e':
                    self.rules[k].remove(el) 
        

    def remove_nongenerative_nonterminals(self):
        keys = list(self.rules.keys())
        grammar_copy = []
        grammar = []
        for non_term in keys:
            for el in self.rules[non_term]:
                if el[0].islower():
                    grammar.append(non_term)
                    break
        while grammar != grammar_copy:
            grammar_copy = grammar
            for non_term in keys:
                for el in self.rules[non_term]:
                    if el[0].islower() or el[0] in grammar_copy:
                        grammar.append(non_term)
        for k in keys:
            if k not in grammar:
                self.rules.pop(k)
                self.nonterminals.remove(k)
   
    def remove_unreachable_nonterminals(self):
        keys = list(self.rules.keys())
        grammar = ['S']
        grammar_copy = []
        while grammar != grammar_copy:
            grammar_copy = grammar
            for nonterminal in grammar_copy:
                if nonterminal in keys:
                    for elem in self.rules[nonterminal]:
                        for el in list(elem):
                            if el.isupper() and el not in grammar:
                                grammar.append(el)
        for el in keys:
            if el not in grammar:
                self.rules.pop(el)
                self.nonterminals.remove(el)
                
                
               
def disappearing_nonterminals(grammar):
    keys = list(grammar.rules.keys())
    disappear = []
    for term in keys:
        for el in grammar.rules[term]:
            if el == 'e':
                vanishings.append(term)

    gr = []
    while gr != disappear:
        gr = disappear
        for term in keys:
            for el in grammar.rules[term]:
                if el.isupper():
                    flag = True
                    for elem in el.split():
                        if elem not in disappear:
                            flag = False
                            break
                    if flag:
                        disappear.append(term)
    return disappear


terminals = ['a', 'b', 'c']
nonterminals=['S', 'A', 'B']
start = 'S'
rules = {'S': ['Ac', 'e', 'a', 'e' ], 'A':['A', 'Sb', 'e'], 'B':['e', 'a']}
#terminals = ['alt', 'cat', 'ast', 'chr', 'nil']
#nonterminals=['S', 'A', 'C', 'I']
#rules = {'S': [['A', 'alt', 'S'], ['A']], 'A':[['C', 'cat', 'A'], ['C']], 'C':[['I', 'ast'], ['I']], 'I':[['nil'], ['chr'], [('S')]]}

print("Initial grammar:")
print(rules)
grammar = CFG(terminals=terminals, nonterminals=nonterminals, start=start, rules=rules)
print("Final grammar without e and unproductive and unreachable non-terminals")
print(grammar.rules)

print("Set of disappeearing nonterminals from the given grammar:")
print(disappearing_nonterminals(grammar))
