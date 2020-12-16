#1) Function for parsing by left recursive method
#2) Parsing using FIRST and FOLLOWS

class CFG:
    def __init__(self, **args):
        self.terminals = args['terminals']
        self.nonterminals = args['nonterminals']
        self.start = args['start']
        self.rules = args['rules']
      
#Function for parsing by left recursive method
def left_recursive_parsing(gr, pair, start_symbol, tree): 
    grammar_rules = gr.rules[start_symbol]
    i = pair[1]
    items = 0
    unwanted = 0
    tree[start_symbol] = []
    for el in grammar_rules:
        for symbol in el:
            items += 1
            if pair[1] >= len(pair[0]):
                return 0
            if symbol in gr.nonterminals: 
                tree[start_symbol].append({})
                flag =  left_recursive_parsing(gr, pair, symbol, tree[start_symbol][len(tree[start_symbol])-1])
                if flag == False:
                    return 0
            else:
                if symbol == pair[0][pair[1]]:
                    tree[start_symbol].append(symbol)
                    pair[1] += 1
                    if(items == len(el)):
                        return 1
                else:
                    pair[1] = i
                    items = 0
                    tree[start_symbol] = []
                    unwanted += 1
                    break
    if unwanted == len(grammar_rules):
        return 0
    else:
        return 1
    
#Parsing using FIRST and FOLLOWS
def get_FIRST(grammar, start_symbol, result):
    grammar_rules = grammar.rules[start_symbol]
    for el in grammar_rules:
        if el[0] in grammar.terminals:
            if el[0] in result:
                continue
            else:
                result.append(el[0])
        else:
            get_FIRST(grammar, el[0], result)


def FIRST(grammar, input_str):
    result = []
    if len(input_str) == 0:
        return result
    if input_str[0] in grammar.terminals:
        result.append(input_str[0])
    else:
        get_FIRST(grammar, input_str[0], result)
    return result

def FOLLOW(grammar, start_symbol):
    result = []
    for symbol in grammar.nonterminals:
        for el in grammar.rules[symbol]:
            if start_symbol in list(el):
                result.extend(FIRST(grammar, el[(el.index(start_symbol)+1):]))
    return list(set(result))


def FIRST_and_FOLLOW_parsing(grammar, pair, start_symbol, tree, check):
    tree[start_symbol] = []
    count = 0
    for rule in grammar.rules[start_symbol]:
        if pair[1] >= len(pair[0]):
            return 0
        if pair[0][pair[1]] in FIRST(grammar, rule):
            count += 1
            for symbol in rule:
                if symbol in grammar.terminals:
                    if symbol == pair[0][pair[1]]:
                        tree[start_symbol].append(pair[0][pair[1]])
                        pair[1] += 1
                    else:
                        return 0
                else: 
                    tree[start_symbol].append(symbol)

                    res = FIRST_and_FOLLOW_parsing(grammar, pair, symbol, tree, check+1)
                    if res == 0:
                        return 0
                    if pair[0][pair[1]] not in FOLLOW(grammar, symbol):
                        return 0
    if count == 0 and (check == 0) and (pair[1] != len(pair[0])):
        return 0 
    return 1


         
def func(grammar, word, rule):
    tree = {}
    if rule =='l':
        result =  left_recursive_parsing(grammar, [word, 0], grammar.start, tree)
    elif rule =='f':
        result = FIRST_and_FOLLOW_parsing(grammar, [word, 0], grammar.start, tree, 0)
    if result:
        return tree
    else:
        return {}


terminals=['a', 'b', 'c', 'd', 'e']
nonterminals=['S', 'A', 'B']
rules={'S': ['cbAa'], 'A': ['aBe', 'e'], 'B': ['dd', 'bd']}
#word = 'cbaddea'
#word = 'cbabdea'
word = 'cbea'

grammar = CFG(nonterminals=nonterminals, terminals=terminals, start='S', rules=rules)
print("Word: ", word)
print("Left recursive parsing:")
print(func(grammar, word, 'l'))
print("Left recursive parsing usinf FIRST and FOLLOWS:")
print(func(grammar, word, 'f'))
