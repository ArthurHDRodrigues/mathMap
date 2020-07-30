from bs4 import BeautifulSoup
import requests, re
from classes import *
from latexUtil import *
import random,math
import pygame

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
		
		
def detPos(node,limite = -200):
    '''
    Recebe um node e muda as pos dos filhos para não ter overlap
    limite = -300
    '''
    limite = -150
    margem = .1
    node.child.sort(key=lambda x: x.size[0], reverse=True)
    i,j = node.pos[0]+1,node.pos[1]-1
    largura = [node.pos[0]+.5 + len(node.name)*0.3]
    '''
    INICIO define qual vai ser a largura
    '''
    #for c in node.child:
    #    largura.append(c.size[0]) #c.pos[0]+
    
    if len(node.child) >= 2:
        limite_horizontal = 1+ node.child[0].size[0] + node.child[1].size[0]+5*margem 
        
        #max(node.pos[0]+.5 + len(node.name)*0.3,10+node.child[0].size[0] +node.child[0].size[1]+2*margem   )#max(largura)
    else:
        limite_horizontal = node.pos[0]+.5 + len(node.name)*0.3
    '''
    FIM define qual vai ser a largura
    '''
    
    '''
    ordena
    '''
    largura = []
    n = len(node.child)
    k=0
    largura_linha = 0
    while k < n:
        if j+node.child[k].size[1] > limite: #dentro do limite vertical
            node.child[k].pos = i,j
            largura_linha = i + node.child[k].size[0]
            #dentro do limite horizontal
            alturas_da_linha = [node.child[k].size[1]]
            
            #dentro do limite horizontal
            k+=1
            while k < n and largura_linha + node.child[k].size[0] + margem <= limite_horizontal:
                node.child[k].pos = largura_linha + margem,j
                largura_linha += node.child[k].size[0]+ margem
                alturas_da_linha.append(node.child[k].size[1])
                
                if node.child[k].size[1] - node.child[k-1].size[1] > 0:
                    #o k-1 é maior 
                    pos_x = node.child[k].pos[0]
                    pos_y = node.child[k].pos[1]
                    
                    altura_sub_bloco = node.child[k].size[1]
                    sub_limite_vertical = node.child[k-1].size[1]
                    
                    t = k+1
                    while t < n:
                        if altura_sub_bloco + node.child[t].size[1] - margem > sub_limite_vertical:
                            node.child.insert(k+1,node.child.pop(t))
                            
                            node.child[k+1].pos = pos_x,pos_y + altura_sub_bloco - margem
                            altura_sub_bloco += node.child[k+1].size[1] - margem
                            k+=1
                        t +=1
                    #thislist.insert(1, "orange")
                    
                elif node.child[k-1].size[1] - node.child[k].size[1] > 0:
                    #o k-1 é menor
                    pos_x = node.child[k-1].pos[0]
                    pos_y = node.child[k-1].pos[1]
                    
                    altura_sub_bloco = node.child[k-1].size[1]
                    sub_limite_vertical = node.child[k].size[1]
                    
                    while k+1 < n and altura_sub_bloco + node.child[k+1].size[1] - margem > sub_limite_vertical:
                        node.child[k+1].pos = pos_x,pos_y + altura_sub_bloco - margem
                        altura_sub_bloco += node.child[k+1].size[1] - margem
                        k += 1
                k+=1
            largura.append(largura_linha)
            j+=min(alturas_da_linha) - margem
            #print('j',j)
        else:
            i = max(largura) + margem
            j = node.pos[1]-1
            
            temp =[]
            for c in node.child[k:]:
                temp.append(c.size[0])
            limite_horizontal+=max(temp)
            
            largura = [i+node.child[k].size[0]]
            node.child[k].pos = i,j
            j+=node.child[k].size[1]- margem
            k+=1
    return node
    
def quebraPalavra(frase, proporcao):
    '''
    string,float -> string
    recebe uma frase e uma proporção e devolve a frase quebrada de tal forma que respeite a proporção
    
    Medições empiricas indicam que cada letra é um retangulo de 3wx4h
     ___
    |   |
    |   |
    |   |
    |___|
    '''
    comprimento = len(frase) #comprimento em pixels
   
    #print('comprimento',comprimento)
    x = math.sqrt(3*comprimento/(4*proporcao))
    c = math.ceil(x)
    f = math.floor(x)
    #print('x',x)
    if c-x > x-f:
      numero_linhas = f
    else:
      numero_linhas = c
        
    altura = numero_linhas*4
    
    largura_bloco = comprimento//numero_linhas
    lista = []
    for i in range(1,numero_linhas+1):
        lista.append(frase[(i-1)*largura_bloco:i*largura_bloco])
        
    lista[-1]+=frase[numero_linhas*largura_bloco:] #cola o resto da string que não gerou um bloco novo
    
    
    #print('numero_linhas',numero_linhas)
    #print('a frase cortada ficou:',lista)

    i=0
    n = numero_linhas-1
    while i< n:
        #print(i)
        if lista[i][-1] == ' ':#detecta se o ultimo char é um espaço e o remove.
            lista[i] = lista[i][:-1]
        elif lista[i+1][0] == ' ':
            lista[i+1] = lista[i+1][1:]#detecta se o primeiro char é um espaço e o remove.
            
        elif lista[i][-1] != ' ' and lista[i+1][0] != ' ': #cortou no meio de uma palavra
           pedaco_esq = lista[i].split(" ")[-1] #pega a metade da direita
           pedaco_dir = lista[i+1].split(" ")[0] #pega a metade da direita
           #print(pedaco_esq)
           #print(pedaco_dir)
           if len(pedaco_esq) > len(pedaco_dir):
               lista[i]+=pedaco_dir
               lista[i+1] = lista[i+1][len(pedaco_dir)+1:]
               if lista[i+1] == '':
                   lista.pop(i+1)
                   i-=1
                   n-=1

           else:
               lista[i+1] = pedaco_esq + lista[i+1]
               lista[i] = lista[i][:-len(pedaco_esq)]
               if lista[i] == '':
                   lista.pop(i)
                   i-=1
                   n-=1
           #print(lista)
        i+=1
    resultado = ''
    len_cada_linha =[]
    n = len(lista)
    for i in range(n-1):
        if lista[i]!='':
            resultado += lista[i]+r'\\ '
            len_cada_linha.append(len(lista[i]))
    resultado+=lista[-1]
    len_cada_linha.append(len(lista[-1]))
    return resultado,max(len_cada_linha),numero_linhas
   
def removeLixo(node):
    proibidos = ['General reference works (handbooks, dictionaries, bibliographies, etc.) pertaining to',
    'Introductory exposition (textbooks, tutorial papers, etc.) pertaining to',
    'Research exposition (monographs, survey articles) pertaining to',
    'Proceedings, conferences, collections, etc. pertaining to',
    'Research data for problems pertaining to',
    'Software, source code, etc. for problems pertaining to',
    'Experimental work for problems pertaining to',
    ]
    n = len(node.child)
    for word in proibidos:
        i=0
        while i<n:
            if word in node.child[i].name:
                node.child.pop(i)
                print("i,",i,"n,",n)
                n-=1
            removeLixo(node.child[i])
            i+=1
        
def organizarNode(node,limite =-150):
    '''
    Node -> None
    Recebe um node e devolve ele de forma que não haja overlap
    pos da raiz = (0,10)
    '''
    for c in node.child:
        organizarNode(c,limite+5)
        
    if node.child != []:
        node.display_name,comprimento,numero_de_linhas = node.name,len(node.name)*0.3,1
    else:
        node.display_name,comprimento,numero_de_linhas = quebraPalavra(node.name, 15)
        comprimento = comprimento*0.25
    
    listaX = [node.pos[0]+.5 + comprimento]
    listaY = [node.pos[1]-0.5*numero_de_linhas]
    node = detPos(node,limite+1)
    for c in node.child:
        listaX.append(c.pos[0]+c.size[0])
        listaY.append(c.pos[1]+c.size[1])
    X = max(listaX, key=abs) - node.pos[0]+0.1
    Y = max(listaY, key=abs) - node.pos[1]-0.1
    
    node.size = (X,Y)
    
    return None
		
def exportToTex(node,file=None):
    '''
    Node,file,(float,float) -> None
    
    Recebe um node, um pontero para arquivo e uma dupla de floats e plota ele num arquivo .tex
    
    o pos é a posição do pai
    '''
    if file == None:
        file = createTex(node.name,(node.size[0]+4,abs(node.size[1])+4))
        beginTikz(file,((0,0),node.size))
        addNodeTikz(file,node)
        for c in node.child:
            exportToTex(c,file)
        endTikz(file)
        closeTex(file)
    else:
        addNodeTikz(file,node)
        for c in node.child:
            exportToTex(c,file)
        

'''
node = Node("raiz")#loadNode("test")
filho1 = Node("filho1")
filho2 = Node("filho2")
filho1.addChild(Node("Ne Bto"))
filho2.addChild(Node("felipe"))

node.addChild(filho1)
node.addChild(filho2)

salveNode(node, "mini")'''

#print(quebraPalavra('Macarronadassãomaisgostosascomarnemoídanomolho', 2))


node = loadNode("half")
#print("############################################")
#print(node)
removeLixo(node)

node.pos = (0,0)

organizarNode(node)
node.updatePos()

exportToTex(node)
#main()
#exportSVG(node)
