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
    temp = r'\draw'+str(node.pos)+' node[anchor=north west] {'+node.name+'};' +'\n'
    file.write(temp)
    if node.child != []:
        temp= r'\draw '+str(node.pos)+' rectangle ('+str(x+a) +','+str(y+b) +');'
        file.write(temp)
    
def main():
    file = createTex("ola_mundo.tex",(10,10))
    beginTikz(file,((-4.1,-1.7),(10.5,2)))
    addNodeTikz(file,"olá, Colli",(0,0))
    endTikz(file)
    closeTex(file)
    
