def treatName(s):
    sub = False
    
    n = len(s)
    #print(n)
    #print(range(n))
    for i in range(n-2):
        #print(i)
        if s[i]+s[i+1] == '\(':
            sub = True
        elif s[i]+s[i+1] == '\)':
            sub = False
        elif sub and s[i] == ' ':
            s = s[:i]+'~'+s[i+1:]
            
    #re.sub('\[[^\]]+\]', '', s)
    return s
    
def removeLixo(node):
    proibidos = ['General reference works (handbooks, dictionaries, bibliographies, etc.) pertaining to',
    'Introductory exposition (textbooks, tutorial papers, etc.) pertaining to',
    'Research exposition (monographs, survey articles) pertaining to',
    'Proceedings, conferences,',
    'Research data for problems pertaining to',
    'Software, source',
    'Experimental work for problems pertaining to'
    ]
    n = len(node.child)
    for word in proibidos:
        i=0
        while i<n:
            if word in node.child[i].name:
                node.child.pop(i)
                #print("i,",i,"n,",n)
                n-=1
            removeLixo(node.child[i])
            i+=1

def countSymbols(frase):
    '''
    string -> list
    Recebe uma string e devolve uma lista, em que cada elemento será um símbolo.
    '''
    inMathMode = False
    ignore = False
    
    lista_sym = []
    n = len(frase)
    i = 0
    
    while i<n-1:
        if frase[i]+frase[i+1] == '\\(':
            inMathMode = True
            if i==0:
                lista_sym.append(0)
            i+=1
        elif frase[i]+frase[i+1] == '\\)':
            inMathMode = False
            i+=1
        elif inMathMode == False:
            lista_sym.append(i)
            
        elif inMathMode == True and frase[i] == '\\':
            ignore=True
            lista_sym.append(i)
        elif inMathMode == True and frase[i] == '^':
            ignore=True
        elif inMathMode == True and (frase[i] == '~' or frase[i] == ','):
            ignore=False
        elif inMathMode == True and (frase[i] == '('or frase[i] == ')'):
            ignore=False
            lista_sym.append(i)
        elif inMathMode == True and ignore == False:
            lista_sym.append(i)
        i+=1
             
    return lista_sym
        



