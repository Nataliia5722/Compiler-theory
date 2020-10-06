import copy

class TransitionSystem:
    
    def __init__(self, **args):
        self.token = args['token']
        self.state = args['state']
        self.start = args['start']
        self.finish = args['finish']
        self.transitions = args['transitions']

    def accept(self, s):
        W = []
        closing = closure(self, ['start'])   #W ← {(s, 0) | s ∈ closure(T , {s∗})};
        closing.remove('start')
        for state in closing:
            W.append((state, 0))
        while len(W)!=0:    #foreach x ∈ W do
            x = W[0]
            W.remove(x)     #W ← W \ {x};
            if x[1] == len(s):  #x_snd = |c|
                for el in W:
                    if el[0] == 'finish' and el[1] == len(s): #x_fst=s*
                        return True                  
            states = []
            for transition in self.transitions:
                if x[1] >= len(s): return False
                if transition[0] == x[0] and transition[1] == s[x[1]]:
                    states.append(transition[2])
            for state in states:              #W ← W ∪ {(s, xsnd + 1) | (xfst, c[xsnd], s) ∈ T};
                W.append((state, x[1]+1))
            closing = copy.copy(W)
            for el in W:
                result = closure(self, [el[0]])   #W ← closure(T , W)
                if len(result) > 1:
                    for i in range(1, len(result)):
                        closing.append((result[i], el[1]))
            W = closing 
        return False
    
    def getTokens(self):
        return set(self.token)

    def getStates(self):
        return set(self.state)

    def print(self):
        print('Set = ', self.token)
      
TransitionSet = [('start', 'e', 'S_even'), ('S_even', 'a', 'S_odd'), ('S_odd', 'a', 'S_even'), ('S_even', 'b', 'S_even'), ('S_odd', 'b', 'S_odd'), ('S_even', 'e', 'finish')]
S=['start', 'finish', 'S_even', 'S_odd']
transitionSystem = TransitionSystem(token=('a','b'), state=('start', 'Seven', 'odd', 'finish'), start='start', finish='finish', transitions=TransitionSet)    

def closure(transition_system, closed_set):
    transitions = copy.copy(transition_system.transitions)

    if len(closed_set) == 0:
        return closed_set
    result = closed_set
    states1 = []
    while(result != states1):  #while W != W` do
        states1 = result       #W` ← W;
        states2 = []
        for t in transitions:
            if t[1] == 'e' and t[0] in states1:
                states2.append(t[2])
                transitions.remove(t)
        result = states1 + states2      #W ← W` ∪ {s ∈ S | (s`, e, s) ∈ T для якогось s` ∈ W`}
    return result     #return W


transitionSystem.print();
print('T = ', TransitionSet)
print('S = ', S)
print('Cheking accept funtion: ')
print('aaab - ', transitionSystem.accept('aaab')) #False
print('aaa - ', transitionSystem.accept('aaa')) #False
print('aaaa - ', transitionSystem.accept('aaaa')) #True
print('ababa - ', transitionSystem.accept('ababa')) #False
print('abababa - ', transitionSystem.accept('abababa')) #True
print('babb - ', transitionSystem.accept('babb')) #False
print('abbabbababb - ', transitionSystem.accept('abbabbababb')) #True
