class Node:
    def __init__(self, name):
        self.name = name
        self.child = []
        self.pos = (0,0)

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
