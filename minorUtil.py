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

def countSymbols(name):
    '''
    string -> int
    Recebe uma string e devolve o comprimeno em digitos após ser renderizada
    '''
    ignore = False
    n=0
    for i in range(len(name)):
        if i == '\\':
            ignore = True
        elif i == ' ':
            ignore = False
        elif ignore == False:
             n+=1
             
    return n
        



