from bs4 import BeautifulSoup
import requests, re
from classes import *
import svgwrite

def main():
	node = baixarArvore()
	salveNode(node, "test")
	print("ok")

def baixarArvore():
	name = input("nome do file:")
	if name == "":
		name = "zbMATH.html"
	with open(name) as fp:
		soup = BeautifulSoup(fp, 'html.parser')

	list = soup.find_all('div')
	for div in list:
		if div.get("class") == ['left']:
			left = div
		elif div.get("class") == ['center']:
			center = div
		elif div.get("class") == ['right']:
			right = div

	sublist = []

	list = left.find_all('div')
	for div in list:
		if div.get("class") == ['half']:
			sublist.append(div.find('a'))

	list = center.find_all('div')
	for div in list:
		if div.get("class") == ['half']:
			sublist.append(div.find('a'))

	list = right.find_all('div')
	for div in list:
		if div.get("class") == ['half']:
			sublist.append(div.find('a'))

	math = Node("math")

	for link in sublist:
		nome = link.string

		if nome == None:
			nome = "K-Theory"

		if nome != "Mathematics education" and nome != "General and overarching topics; collections":
			ramo = foo(nome, link.get('href'))
			math.addChild(ramo)
			print(nome,": ok")
	return math

def foo(nome, link):
	'''
	string, string -> Node
	recebe o nome de uma área da matematica e um link para ela e devolve o
	Node dela junto aos Nodes das subareas
	'''
	r = Node(nome)
	page = requests.get(link, timeout=50)
	soup = BeautifulSoup(page.text, 'html.parser')
	subsoup = soup.find(id="classification")

	list = subsoup.find_all('div')
	layer_1 = Node("temp")

	for div in list:
		if div.get("class") == ['item', 'level1']:
			lista_de_a = div.find_all('a')
			layer_1 = Node(lista_de_a[1].text)
			r.addChild(layer_1)


		elif div.get("class") == ['item', 'level2']:
			lista_de_a = div.find_all('a')
			nome = lista_de_a[1].text

			if nome != "None of the above, but in this section":
				fil = Node(nome)
				layer_1.addChild(fil)
	return r


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

	tamanho = len(f)
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


def treatName():
	return re.sub('\[[^\]]+\]', '', s)

def exportSVG(node=None):
	'''
	Node -> None

	recebe uma árvore e gera um arquivo svg
	'''
	W = 1000
	H = 1000
	dwg = svgwrite.Drawing('test.svg',(W,H), profile='tiny')
	#dwg.add(dwg.line((0, 0), (100, 0), stroke=svgwrite.rgb(10, 10, 16, '%')))

	'''dwg.add(dwg.text(node.name, insert=(1, 10), fill='black'))
	for i in range(len(node.child)):
		y = 1
		dwg.add(dwg.text(node.child[i].name, insert=(5, (i+2)*10), fill='black'))'''

	dwg.add(dwg.rect(insert=(0, 0), size=(W,H),fill='white'))
	drawRecursive(dwg,node,(5,10))
	dwg.save()

def drawRecursive(dwg, node, xy):
	dwg.add(dwg.text(node.name, insert=xy, fill='black'))
	x,y = xy
	u = sum(1 for c in node.name if c.isupper())
	n = len(node.name)
	dwg.add(svgwrite.shapes.Rect(insert=(x-3,y-11),size=(10*u+5*(n-u),14),fill="none", stroke="black"))

	for i in range(len(node.child)):
		y+=16*node.child[i].countProli()
		drawRecursive(dwg, node.child[i], (x+5,y))

'''
node = Node("raiz")#loadNode("test")
filho1 = Node("filho1")
filho2 = Node("filho2")
filho1.addChild(Node("Ne Bto"))
filho2.addChild(Node("felipe"))

node.addChild(filho1)
node.addChild(filho2)

salveNode(node, "mini")'''

node = loadNode("mini")
#print("############################################")
print(node)
#main()
#exportSVG(node)
