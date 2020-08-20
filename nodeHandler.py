from classes import *

def salveNode(node, filename):
	'''
	Node, string -> None
	'''
	fl = filename + ".txt"
	f = open(fl, "wt")

	f.write(node.store())
	f.close()

def countPlus(word):
	'''
	string -> int
	recebe uma string e revolve o n° de '+' no inicio dela
	'''
	i=0
	n=0
	while word[i]=='+':
	    n+=1
	    i+=1

	return n

def loadNode(file):
	'''
	string -> Node
	'''
	#print("============")
	if isinstance(file, str):
		fl = file + ".txt"
		temp = open(fl, "rt")
		f = temp.readlines()
		temp.close()
	else:
		f = file

	#tamanho = len(f)
	current = f.pop(0)
	n = countPlus(current)
	current = current[n:-1]
	node = Node(current)
	if f != []:
		m = countPlus(f[0])
		while n+1 == m:
			node.addChild(loadNode(f))
			if f != []:
				m = countPlus(f[0])
			else:
				break

	return node
