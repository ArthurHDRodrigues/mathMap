class Node:
    def __init__(self, name):
        self.name = name
        self.child = []
        self.pos = (0,0)
        self.size = (0,0) #offset para somar com pos, o retangulo pos-size cobre o Node

    def __str__(self,spacer="   "):
        if self.child == []:
            r = self.name
        else:
            r = self.name+":"
        for i in self.child:
            r+="\n"+spacer+i.__str__(spacer+spacer)
        return r


    def addChild(self, newchild):
        self.child.append(newchild)


    def updateName(self, newname):
        self.name = newname

    def store(self,spacer="+"):
        r = self.name
        for i in self.child:
            r+="\n"+spacer+i.store(spacer+'+')
        return r

    def countProli(self):
        '''
        Node -> int

        devolve o número de vértices da árvore
        '''
        r = 1
        for c in self.child:
            r += c.countProli()
        return r
        
    def updatePos(self):
        '''
        calcula a posição absoluta de cada nó
        '''
        for c in self.child:
            c.pos = c.pos[0]+self.pos[0],c.pos[1]+self.pos[1]
            c.updatePos()
        
    
def updatePosAndSize(node):
    '''
    Node -> float
    '''
    lista = []
    for i in node.child:
        lista.append(i.updatePosAndSize())
        
    node.child = organizaCaixas(node.child)
    temp = []
    for i in node.child:
        temp.append(i.pos.y+i.size.y)
        #x+= random.uniform(0, 1)
        #y-= random.uniform(.7, 1.7)
            
    #size = 
    return max(lista)
