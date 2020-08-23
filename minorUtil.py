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
    lista_sym = []
    n = len(frase)
    i = 0
        
    while i<n-1:
        
        if frase[i]+frase[i+1] == r'\(':
            j = i+1
            while j<n and (frase[j]!= '~' and frase[j-1] + frase[j] != r'\)'): #and frase[j] != r'('):
                #print(frase[j-1] + frase[j])
                #print(frase[j-1] + frase[j] != r'\)')
                j+=1
            lista_sym.append(frase[i:j+1])
            i=j
        else:
            lista_sym.append(frase[i])
        i+=1
    if i == n-1:
        lista_sym.append(frase[i])
    return lista_sym

