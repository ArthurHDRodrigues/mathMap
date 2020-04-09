from bs4 import BeautifulSoup
import requests, re
from classes import *
import svgwrite

def main():
	#node = baixarArvore()
	#salveNode(node, "test")
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
	recebe o nome de uma área da matematica e um link para ela e devolve o Node dela junto aos Nodes das subareas
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

def loadNode(filename):
	'''
	string -> Node
	'''
	fl = filename + ".txt"
	f = open(fl, "wt")

	f.read(node.store())
	f.close()
	return 0


def treatName():
	return re.sub('\[[^\]]+\]', '', s)

def exportSVG(node=None):
	'''
	Node -> None

	recebe uma árvore e gera um arquivo svg
	'''
	dwg = svgwrite.Drawing('test.svg',(100,100), profile='tiny')
	#dwg.add(dwg.line((0, 0), (100, 0), stroke=svgwrite.rgb(10, 10, 16, '%')))

	'''dwg.add(dwg.text(node.name, insert=(1, 10), fill='black'))
	for i in range(len(node.child)):
		y = 1
		dwg.add(dwg.text(node.child[i].name, insert=(5, (i+2)*10), fill='black'))'''

	drawRecursive(dwg,node,(5,10))
	dwg.save()

def drawRecursive(dwg, node, xy):
	dwg.add(dwg.text(node.name, insert=xy, fill='black'))
	x,y = xy
	dwg.add(svgwrite.shapes.Rect(insert=(x-3,y-11),size=(6*len(node.name),14),fill="none", stroke="black"))

	for i in range(len(node.child)):
		y+=16*node.child[i].countProli()
		drawRecursive(dwg, node.child[i], (x+5,y))

node = Node("raiz")
filho1 = Node("filho1")
filho2 = Node("filho2")
filho1.addChild(Node("Neto"))
filho2.addChild(Node("felipe"))

node.addChild(filho1)
node.addChild(filho2)
exportSVG(node)
