#класс для построения связного списка
class Node:
 def __init__(self, left_child_index):
  self.DataValue = ""
  self.LeftChild = left_child_index
  self.RightChild = -1

#класс для представления дерева регулярного выражения
class ReX:
 def __init__(self):
  self.Tree = list()
  for index in range(1, 21):
   self.Tree.append(Node(index))
  self.Fringe = list()
  self.Root = 0
  self.NextFreeChild = 0
  #проверка, является ли символ оператором
 def IsOperator(self, s):
  if '+' in s:
   return True
  if '-' in s:
   return True
  if '*' in s:
   return True
  if '/' in s:
   return True
  return False
 #вставка узла в бинарное дерево
 def Insert(self, NewToken):
  if self.NextFreeChild == -1: # проверка если дерево полное
   return "Tree is Full"
 # вставка нового токена
  if self.NextFreeChild == 0:
   self.Tree[self.Root].DataValue = NewToken
   self.NextFreeChild = self.Tree[self.Root].LeftChild
   self.Tree[self.Root].LeftChild = -1
  else:
  # начало с корня, вставка узлов
   Current = 0 # индекс текущего узла
   Previous = -1 # индекс предыдущего узла
   NewNode = self.Tree[self.NextFreeChild] # создание нового узла
   NewNode.DataValue = NewToken
  # поиск узла, после которого можно добавить новый узел
   while Current != -1:
    CurrNode = self.Tree[Current]
   # проверка CurrNode на содержание оператора
    if self.IsOperator(CurrNode.DataValue):
    # если LeftChild пуст, вставка в него
     if CurrNode.LeftChild == -1:
      CurrNode.LeftChild = self.NextFreeChild
      self.NextFreeChild = NewNode.LeftChild
      NewNode.LeftChild = -1
      Current = -1
    # если RightChild пустой, вставка в него
     elif CurrNode.RightChild == -1:
      CurrNode.RightChild = self.NextFreeChild
      self.NextFreeChild = NewNode.LeftChild
      NewNode.LeftChild = -1
      Current = -1
    # если LeftChild оператор
    # переместить LeftChild-поддерево
     elif self.IsOperator(self.Tree[CurrNode.LeftChild].DataValue):
      Previous = Current
      Current = CurrNode.LeftChild
      self.Fringe.append(Previous)
    # если RightChild оператор
    # переместить RightChild-subtree
     elif self.IsOperator(self.Tree[CurrNode.RightChild].DataValue):
      Previous = Current
      Current = CurrNode.RightChild
      self.Fringe.append(Previous)
    # переместить right-subtree
     else:
      Previous = self.Fringe.pop(-1)
      Current = self.Tree[Previous].RightChild
   # нет места для вставки
    else:
     return "Cannot be inserted"

#Эта функция просматривает весь массив Tree и отображает индекс каждого элемента массива и значение узла.
 def Display(self):
  for index in range(len(self.Tree)):
   print("Index: ", index, "DataValue: ",self.Tree[index].DataValue)


 def Infix(self, root, arr):
  if root.DataValue != "":
   if self.IsOperator(root.DataValue):
    arr.append('(')
   self.Infix(self.Tree[root.LeftChild], arr)
   arr.append(root.DataValue)
   self.Infix(self.Tree[root.RightChild], arr)
   if self.IsOperator(root.DataValue):
    arr.append(')')
#проверка работы программы, подсчет значения арифметического выражения
 def calculate(self, expression):
  def processing(left, stack):
   right = stack.pop() # получить число справва
  # print(right)
   right = int(right)
   operator = stack.pop() # получить оператор
  # print(operator)
   left = stack.pop() # число слева
   left = int(left)
  # вычисление в зависимости от оператора
   if '+' in operator:
    left += right
   elif '-' in operator:
    left -= right
   elif '*' in operator:
    left *= right
   elif '/' in operator:
    left /= right
   return left, stack
  stack = []
  count = 0
  left = 0
  for char in expression:
   stack.append(char)
   if char == ')':
    stack.pop()
    left, stack = processing(left, stack)
    stack.pop()
    stack.append(left)
   if count == len(expression)-1: # последний символ строкового выражения
    left, stack = processing(left, stack)
   count += 1
  return left

#функция для вывода дерева на экран в виде строки 
def __str__():
 arr = []
 expressionTree.Infix(expressionTree.Tree[0], arr)
 expression_string = ''.join(arr[1:-1])
 print(expression_string)


import re
#ввод регулярного выражения (b*(c/d))+a
expressionTree = ReX()
expressionTree.Insert('+')
expressionTree.Insert('*')
expressionTree.Insert('a')
expressionTree.Insert('b')
expressionTree.Insert('/')
expressionTree.Insert('c')
expressionTree.Insert('d')
print('Представление хранения дерева в программе:')
expressionTree.Display()

#вызов функции для вывода дерева на экран в виде строки
print('Регулярное выражение:')
__str__()

#роверка работы алгоритма на основе арифметических выражений
#regex_expression = "[\/\+\-\*\(\)]|[0–9][0–9][0–9]|[0–9][0–9]|[0–9]"
#txt_list = re.findall(regex_expression, "(2*(3/1))+4")
#print(expressionTree.calculate(txt_list))
#txt_list = re.findall(regex_expression, "2+4")
#print(expressionTree.calculate(txt_list))
#txt_list = re.findall(regex_expression, "(2+4)-1")
#print(expressionTree.calculate(txt_list))
#txt_list = re.findall(regex_expression, "(10-(2+4)")
#print(expressionTree.calculate(txt_list))


