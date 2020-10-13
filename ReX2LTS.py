
class TransitionSystem:
    def __init__(self, **args):
        self.token = args['token']
        self.state = args['state']
        self.start = args['start']
        self.finish = args['finish']
        self.transitions = args['transitions']

    def to_lts(s, **args):
        operation = args['operation']
        value = args['value']
        
        if operation == 'null':
            lts = TransitionSystem(token=[], state=['start', 'finish'], start='start', finish='finish', transitions=[])
            if value[0] == 'e':
                lts.transitions.append(('start', 'e', 'finish'))
            else:
                lts.token.append(value[0])
                lts.transitions.append(('start', value[0], 'finish'))
            return lts
        elif operation == '*':
            if 0 in value:
                lts2 = TransitionSystem.to_lts(s, operation='null', value=value)
            else:
                operation = list(value.keys())[0]
                lts2 = TransitionSystem.to_lts(s, operation=operation, value=value[operation])
            start1 = ('s_'+ str(s))
            s+=1
            finish1 = ('s_'+ str(s))
            s+=1
            lts2.state+= [start1, finish1]
            transitions = []
            for el in lts2.transitions:
                if el[0] == 'start' and el[2] == 'finish':
                    transitions.append((start1, el[1], finish1))
                elif el[0] == 'start':
                    transitions.append((start1, el[1], el[2]))
                elif el[2] == 'finish':
                    transitions.append((el[0], el[1], finish1))
                else:
                    transitions.append((el[0], el[1], el[2]))

            transitions.append(('start', 'e', start1))
            transitions.append((finish1, 'e', 'finish'))
            transitions.append((start1, 'e', finish1))
            transitions.append((finish1, 'e', start1))
            lts2.transitions = transitions
            return lts2
        elif operation in ['|', ',']:
            if 0 in value['left']:
                lts3 = TransitionSystem.to_lts(s, operation='null', value=value['left'])
            else:
                operation = list(value['left'].keys())[0]
                lts3 = TransitionSystem.to_lts(s, operation=operation, value=value['left'][operation])
            if 0 in value['right']:
                lts4 = TransitionSystem.to_lts(s, operation='null', value=value['right'])
            else:
                operation = list(value['right'].keys())[0]
                lts4 = TransitionSystem.to_lts(s, operation=operation, value=value['right'][operation])
            if operation == ',':
                finishLeft = ('s_'+ str(s))
                s+=1
                rightStart = ('s_'+ str(s))
                s+=1
                lts3.state += [finishLeft, rightStart]
                lts3.state += lts4.state
                lts3.state.remove('start')
                lts3.state.remove('finish')
                lts3.token += lts4.token
                transitions = []
                for el in lts3.transitions:
                    if el[2] == 'finish':
                        transitions.append((el[0], el[1], finishLeft))
                    else:
                        transitions.append((el[0], el[1], el[2]))
                for el in lts4.transitions:
                    if el[0] == 'start':
                        transitions.append((rightStart, el[1], el[2]))
                    else:
                        transitions.append((el[2], el[1], el[2]))
            
                transitions.append((finishLeft, 'e', rightStart))
                lts3.transitions = transitions
                return lts3
            elif operation == '|':
                leftStart = ('s_'+ str(s))
                s+=1
                finishLeft = ('s_'+ str(s))
                s+=1
                rightStart = ('s_'+ str(s))
                s+=1
                rightFinish = ('s_'+ str(s))
                s+=1
                lts3.state += [leftStart, finishLeft, rightStart, rightFinish]
                lts3.state += lts4.state
                lts3.state.remove('start')
                lts3.state.remove('finish')
                lts3.token += lts4.token
                transitions = []
                for el in lts3.transitions:
                    if el[0] == 'start' and el[2] == 'finish':
                        transitions.append((leftStart, el[1], finishLeft))
                    elif el[0] == 'start':
                        transitions.append((leftStart, el[1], el[2]))
                    elif el[2] == 'finish':
                        transitions.append((el[0], el[1], finishLeft))
                    else:
                        transitions.append((el[0], el[1], el[2]))
                for el in lts4.transitions:
                    if el[0] == 'start' and el[2] == 'finish':
                        transitions.append((rightStart, el[1], rightFinish))
                    elif el[0] == 'start':
                        transitions.append((rightStart, el[1], el[2]))
                    elif el[2] == 'finish':
                        transitions.append((el[0], el[1], rightFinish))
                    else:
                        transitions.append((el[0], el[1], el[2]))
            
                transitions.append(('start', 'e', leftStart))
                transitions.append(('start', 'e', rightStart))
                transitions.append((finishLeft, 'e', 'finish'))
                transitions.append((rightFinish, 'e', 'finish'))
                lts3.transitions = transitions
                return lts3

        
class ReX:
    def __init__(self, **args):
        self.tree = {}

        if len(args) == 0:
            self.tree[0] = 'e'
        elif 'token' in args:
            self.tree[0] = args['token']
        elif 'operation' in args and 'expressions' in args:
            if args['operation'] == '*':
                if len(args['expressions']) != 1:
                    print('Введено неверное количество элементов.')
                elif 0 in args['expressions'][0].tree and args['expressions'][0].tree[0] == 'e':
                    print('Некорректный ввод')
                else:
                    self.tree['*'] = args['expressions'][0].tree
            elif args['operation'] in ('|', ','):
                if len(args['expressions']) != 2:
                    print('Введено неверное количество элементов.')
                else:
                    self.tree[args['operation']] = { 'left': args['expressions'][0].tree, 'right': args['expressions'][1].tree }
        else:
            print('Некорректный ввод')

    def toString(tree) -> str:
        string = ''

        if 0 in tree:
            if tree[0] == 'e':
                string += ''
            else:
                string += tree[0]
        elif ',' in tree:
            string += '('
            ReX.toString(tree[',']['left'])
            string += ','
            ReX.toString(tree[',']['right'])
            string += ')'
        elif '|' in tree:
            string += '('
            ReX.toString(tree['|']['left'])
            string += '|'
            ReX.toString(tree['|']['right'])
            string += ')'
        elif '*' in tree:
            ReX.toString(tree['*'])
            string += '*'
    
        
    def __str__(self):
        return str(ReX.toString(self.tree))


def ReX2LTS(rex):
    s=0
    if 0 in rex.tree: 
        return TransitionSystem.to_lts(s, operation='null', value=rex.tree)
    else:
        next_operation = list(rex.tree.keys())[0]
        return TransitionSystem.to_lts(s, operation=next_operation, value=rex.tree[next_operation])

rex = ReX(token='a') 
print('Выражение: a')
lts = ReX2LTS(rex)
print('LTS: ', lts.transitions)


rex2 = ReX(operation='|',  expressions=[ReX(token='a'), ReX(token='b')])
print('Выражение: (a|b)')
lts = ReX2LTS(rex2)
print('LTS: ', lts.transitions)

rex3 = ReX(operation=',', expressions=[rex2, ReX(token='c')])
print('Выражение: ((a|b),c) ')
lts = ReX2LTS(rex3)
print('LTS: ', lts.transitions)
