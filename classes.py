class Node:
    def __init__(self, name):
        self.name = name
        self.child = []

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
