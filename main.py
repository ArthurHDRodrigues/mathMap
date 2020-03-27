from bs4 import BeautifulSoup
import requests, re
from classes import *


def main():
	node = baixarArvore()

	salveNode(node, "test")


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

main()
