from header import *
import random,math

def main():
	node = baixarArvore()
	salveNode(node, "test")
	print("ok")
        
def detPos(node,limite = -200):
    '''
    Recebe um node e muda as pos dos filhos para não ter overlap
    limite = -300
    '''
    #limite = -150
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
        #limite_horizontal = 1+ node.child[0].size[0] + node.child[1].size[0]+5*margem 
        
        switcher = {
            0: 0.51, 
            1: 0.432,
            2: 0.37
            }
        
        x = node.pos[0]+.5 + len(node.name)*switcher.get(node.depth,"default")
        y = node.child[0].size[0] +node.child[1].size[0]+2*margem
        
        limite_horizontal = max( x , y )#max(largura)
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
    #print('n',n)
    while k < n:
        if j+node.child[k].size[1] > limite: #dentro do limite vertical
            
            node.child[k].pos = i,j
            
            largura_linha = i + node.child[k].size[0]
            alturas_da_linha = [node.child[k].size[1]]
            
            #dentro do limite horizontal
            index_ultimo_horizontal = k
            altura_sub_bloco = node.child[index_ultimo_horizontal].size[1]
            k+=1
            l=k
            while l<n:
                if k<n and l<n and largura_linha + node.child[l].size[0] + margem <= limite_horizontal:
                    node.child.insert(k,node.child.pop(l))
                    
                    node.child[k].pos = largura_linha + margem,j
                    
                    largura_para_add = node.child[k].size[0]+margem
                    alturas_da_linha.append(node.child[k].size[1])
                    
                    
                    k+=1
                    if node.child[k-1].size[1] - node.child[index_ultimo_horizontal].size[1] > 0:
                        #o da direita (k-1) é menor
                        
                        pos_x = node.child[k-1].pos[0]
                        pos_y = node.child[k-1].pos[1]
                    
                        altura_sub_bloco = node.child[k-1].size[1]
                        sub_limite_vertical = node.child[index_ultimo_horizontal].size[1]
                        index_ultimo_horizontal = k-1
                        #print('valor inicial de k',k)
                        for t in range(k,n):
                            if altura_sub_bloco + node.child[t].size[1] - margem > sub_limite_vertical and largura_linha + node.child[t].size[0] + margem <= limite_horizontal:
                                l+=1
                                node.child.insert(k,node.child.pop(t))
                                node.child[k].pos = pos_x,pos_y + altura_sub_bloco - margem
                                altura_sub_bloco += node.child[k].size[1] - margem
                                k+=1
                    
                        
                    
                    elif altura_sub_bloco - node.child[k-1].size[1] > 0:
                        #o da esquerda (index_ultimo_horizontal) é menor
                        pos_x = node.child[index_ultimo_horizontal].pos[0]
                        pos_y = node.child[index_ultimo_horizontal].pos[1]
                        #altura_sub_bloco = node.child[index_ultimo_horizontal].size[1]
                        sub_limite_vertical = node.child[k-1].size[1]
                        index_ultimo_horizontal = k-1
                        for t in range(k,n):
                            if altura_sub_bloco + node.child[t].size[1] - margem > sub_limite_vertical:
                            
                                if node.child[t].name == "Exponential sums and character sums":
                                    print(node.child[index_ultimo_horizontal].name)
                                l+=1
                                node.child.insert(k,node.child.pop(t))
                                node.child[k].pos = pos_x,pos_y + altura_sub_bloco - margem
                                altura_sub_bloco += node.child[k].size[1] - margem
                                k+=1
                        
                        altura_sub_bloco = node.child[index_ultimo_horizontal].size[1]
                    else:
                        index_ultimo_horizontal = k-1
                    largura_linha+= largura_para_add
                l+=1
                            
                    
            largura.append(largura_linha)
            j+=min(alturas_da_linha) - margem
            
        else:
            i = max(largura) + margem
            j = node.pos[1]-1
            
            temp =[]
            for c in node.child[k:]:
                temp.append(c.size[0])
            limite_horizontal+=max(temp)
            
            largura = [i+node.child[k].size[0]]
            #print('k',k)
            #print('k',k,node.child[k].name)
            node.child[k].pos = i,j
            j+=node.child[k].size[1]- margem
            k+=1
    return node
    
def quebraPalavra(frase, proporcao):
    '''
    string,float -> string
    recebe uma frase e uma proporção e devolve a frase quebrada de tal forma que respeite a proporção
    
    Medições empiricas indicam que cada letra é um retangulo de 3wx4h
    '''
    frase = treatName(frase) #troca espaços por ~ no mathmode
    lista_sym = countSymbols(frase)
    comprimento = len(lista_sym) #conta quantos simbolos teremos após renderizar
   

    x = math.sqrt(3*comprimento/(4*proporcao)) #calcula a altura da caixa, a proporção de um símbolo é 3/4
    c = math.ceil(x)
    f = math.floor(x)
    
    if c==0:
        numero_linhas = f
    elif f==0:
        numero_linhas = c
    elif c-x > x-f:
      numero_linhas = f
    else:
      numero_linhas = c
    
    
    
    largura_bloco = comprimento//numero_linhas
    lista_de_linhas = []
    n = numero_linhas-1
    #print('numero_linhas',numero_linhas)
    #print('comprimento',comprimento)
    #print('largura_bloco',largura_bloco)
    for i in range(n):
        lista_de_linhas.append(lista_sym[(i)*largura_bloco : (i+1)*largura_bloco])
    
    lista_de_linhas.append(lista_sym[n*largura_bloco:])

    print(lista_de_linhas)
    i=0
    while i< n:
        #cortou no meio de uma palavra   
        if lista_de_linhas[i+1][0] != ' ' and lista_de_linhas[i][-1] != ' ':
            m = len(lista_de_linhas[i])
            e = m
            while e > 0 and lista_de_linhas[i][e-1] != ' ':
                e-=1
            pedaco_esq = lista_de_linhas[i][e:] #pega a metade da esquerda
            #print('pedaco_esq',pedaco_esq,e)
            
            d = 0
            l = len(lista_de_linhas[i+1])
            while d<l and lista_de_linhas[i+1][d] != ' ':
                d+=1
            pedaco_dir = lista_de_linhas[i+1][:d] #pega a metade da direita
            #print('pedaco_dir',pedaco_dir,d)

            if m-e > d:
                lista_de_linhas[i] += pedaco_dir
                lista_de_linhas[i+1] = lista_de_linhas[i+1][d:]
               
                if lista_de_linhas[i+1] == []:
                    lista_de_linhas.pop(i+1)
                    i-=1
                    n-=1

            else:
                lista_de_linhas[i+1] = pedaco_esq + lista_de_linhas[i+1]
                lista_de_linhas[i] = lista_de_linhas[i][:-(m-e)]
                if lista_de_linhas[i] == []:
                    lista_de_linhas.pop(i)
                    i-=1
                    n-=1
        i+=1
        
        
    resultado = ''
    len_cada_linha = []
    n = len(lista_de_linhas)
    #print(lista_de_linhas)
    i=0
    while i<n:
        #print(i,lista_de_linhas[i])
        if lista_de_linhas[i] == []:
            lista_de_linhas.pop(i)
            n-=1
        elif lista_de_linhas[i] == [' ']:
            lista_de_linhas.pop(i)
            n-=1
        else:
            #detecta se o ultimo char é um espaço e o remove.
            if lista_de_linhas[i][-1] == ' ':
                lista_de_linhas[i].pop(-1)
            
            #detecta se o primeiro char é um espaço e o remove.  
            elif lista_de_linhas[i][0] == ' ':
                lista_de_linhas[i].pop(0)
            
            m = len(lista_de_linhas[i])
            print('m',m)
            len_cada_linha.append(m)
            for j in range(m):
                resultado+=lista_de_linhas[i][j]
            if i<n-1:
                resultado+=r'\\ '
            i+=1
        
        

    return resultado,max(len_cada_linha),n
        
def organizarNode(node,limite =-150):
    '''
    Node -> None
    Recebe um node e devolve ele de forma que não haja overlap
    pos da raiz = (0,10)
    '''
    for c in node.child:
        organizarNode(c,limite+5)
    
    
    if node.depth == 2 and node.child == []:
        node.display_name,comprimento,numero_de_linhas = quebraPalavra(node.name, 5)
        comprimento = comprimento*.31
        
    elif node.depth != 3:
        switcher = {
            0: 0.51, 
            1: 0.432,
            2: 0.31
            }
        node.display_name = node.name
        comprimento = len(node.name)*switcher.get(node.depth,"default")
        numero_de_linhas = 1
        #print(node.name,":",switcher.get(node.depth,"default"))
    else:
        node.display_name,comprimento,numero_de_linhas = quebraPalavra(node.name, 2) #15
        comprimento = comprimento*.25
    
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
        

'''
node = Node("raiz")#loadNode("test")
filho1 = Node("filho1")
filho2 = Node("filho2")
filho1.addChild(Node("Ne Bto"))
filho2.addChild(Node("felipe"))

node.addChild(filho1)
node.addChild(filho2)

salveNode(node, "mini")'''


#s = 'aabb\(\oi tchau\) uu'
#print(treatName(s))

node = loadNode("half/half")
node.pos = (0,0)
removeLixo(node)
node.updateDepth()
organizarNode(node)
node.updatePos()
exportToTex(node)

#f = 'Inertial manifolds'
#print(quebraPalavra(f, 2))
'''
x = '\((\infty,1)\)-categories (quasi-categories, Segal spaces, etc.); \(\infty\)-topoi, stable \(\infty\)-categories'
h = 'Convexity properties of solutions to PDEs and systems of PDEs with constant coefficients'   
s = 'Boundary value problems for systems of linear higher-order PDEs'

print(countSymbols(x))'''


