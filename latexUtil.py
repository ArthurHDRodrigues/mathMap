from classes import *
def createTex(name,size):
    '''
    string -> file
    
    retorna um objeto de arquivo, em modo write, com cabeçalho e nome name 
    '''
    fonte = "Cousine"
    file = open(name+".tex","w")
    header = r"\documentclass[12pt]{article}"
    header += "\n"
    header += r"\usepackage[utf8]{inputenc}"
    header += "\n"
    header += r"\usepackage{pgf,tikz,pgfplots}"+"\n"+r"\pgfplotsset{compat=1.15}"+"\n"+r"\usepackage{mathrsfs}"+"\n"+r"\usetikzlibrary{arrows}"
    header += "\n"
    header += r'\usepackage{fontspec}'+"\n"+'\setmainfont[Renderer=ICU,Mapping=tex-text]{'+fonte+'}'
    header += "\n"
    header +=r'\usepackage{amssymb}'
    header += "\n"
    x,y = size
    header += r"\usepackage[paperwidth="+str(x)+"cm,paperheight="+str(y)+"cm,left=0.1cm,right=0.1cm,top=0.1cm,bottom=0.1cm]{geometry}"
    header += "\n"
    file.write(header)
    
    
    file.write(r"\begin{document}")
    header += "\n"
    
    return file
    
def closeTex(file):
    file.write('\n')
    file.write(r"\end{document}")
    file.close()
    return None
    
    
def beginTikz(file,size):
    '''
    file, dupla -> None
    
    '''
    x,y = size
    file.write(r'\begin{tikzpicture}[line cap=round,line join=round,>=triangle 45,x=1cm,y=1cm]')
    file.write("\n")
    temp = r'\clip'+str(x)+'rectangle'+str(y)+';'
    file.write(temp)
    file.write("\n")
    return None
    
def endTikz(file):
    file.write("\n")
    file.write(r'\end{tikzpicture}')
    file.write("\n")
    return None
    
def addNodeTikz(file,node):
    x = node.pos[0]
    y = node.pos[1]
    a = node.size[0]
    b = node.size[1]
    
    file.write("\n")
    
    switcher = {
    0: '\Huge ',  
    1: '\LARGE ',
    2: '\large ',
    3: ''
    }
    color = {
    0: 'black!10',  
    1: 'black!20',
    2: 'black!30',
    3: 'black!40'
    }
    #value = switcher.get(key, "default")
    temp = r'\filldraw [color=black,fill='+color.get(node.depth,"default")+']'+str(node.pos)+' rectangle ('+str(x+a) +','+str(y+b) +');\n'
    temp += r'\draw'+str(node.pos)+' node[anchor=north west,align=left] {'
    
    ultimo = node.display_name.pop(-1)
    for linha in node.display_name:
        temp += switcher.get(node.depth,"default")+linha+r'\\ '
        
    temp+= switcher.get(node.depth,"default")+ultimo
    temp+='};' +'\n'
    
    file.write(temp)
    
        
def exportToTex(node,file=None):
    '''
    Node,file,(float,float) -> None
    
    Recebe um node, um pontero para arquivo e uma dupla de floats e plota ele num arquivo .tex
    
    o pos é a posição do pai
    '''
    if file == None:
        file = createTex(node.name+'/'+node.name,(node.size[0]+4,abs(node.size[1])+4))
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
def main():
    file = createTex("ola_mundo.tex",(10,10))
    beginTikz(file,((-4.1,-1.7),(10.5,2)))
    addNodeTikz(file,"olá, Colli",(0,0))
    endTikz(file)
    closeTex(file)
    
