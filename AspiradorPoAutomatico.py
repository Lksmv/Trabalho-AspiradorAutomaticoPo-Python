import random as rd
import matplotlib.pyplot as plt

def main():   #Main 
    agente = input("Escolha: Agente Reativo Simples '0' ou Agente Baseado em Objetivo '1' ") #pergunta
    matrix = definirAmbiente() #cria ambiente
    for z in matrix:#exibe no console o ambiente
        print(z)
    posicao = [1,1] #posicao inicial
    pontos = 0 #inicia variavel pontos
    acao = 0 #inicia variavel acao
    if( agente == '1'): #Agente baseado em objetivo
        estado = estadoAtual(matrix,posicao) #estado na posicao atual
        percepcao = [posicao,estado] #percepcao contendo posicao + estado
        exibir(matrix,percepcao[0]) #exibe o ambiente
        while(acao != 6): #enquanto o objetivo não for alcançado
            acao = agenteObjetivo(matrix,percepcao,checkObj(matrix)) #salva a acao que o aspirador deve tomar
            if(acao != 6): # se não for para o aspirador parar
                pontos +=1 #contar pontos
                percepcao = executarAcao(matrix,percepcao,acao) #executaacao
                exibir(matrix,percepcao[0]) #exibe mapa
        print('pontuação total: '+str(pontos)) #printa os pontos
    elif(agente == '0'): #Agente Reativo Simples
        posicao= [rd.choice([1,2,3,4]),rd.choice([1,2,3,4])] #posicao inicial aleatoria do aspirador 
        estado = estadoAtual(matrix,posicao) #estado
        percepcao = [posicao,estado] #percepcao contendo posicao + estado
        exibir(matrix,percepcao[0]) #exibir
        mapa = funcaoMapear() # funcaoMapear
        while True: #loop
            percepcao = executarAcao(matrix,percepcao, agenteReativoSimples(matrix,mapa,percepcao))  #percepcao do robo apos executar acao      
            exibir(matrix,percepcao[0]) #exibir
    
    
def exibir(I, posicao):    
    plt.imshow(I)
    plt.nipy_spectral() 
    plt.plot(posicao[0],posicao[1], marker='H', color='r', ls='')
    plt.pause(0.25)    
    plt.clf()
    
def definirAmbiente(): # Define o ambiente, onde 1 = parede, 0 = limpo, 2 = sujo (sendo que as posições da sujeira são aleatorias)
    matrix = [[1,1,1,1,1,1],
              [1,rd.choice([0,2]),rd.choice([0,2]),rd.choice([0,2]),rd.choice([0,2]),1],
              [1,rd.choice([0,2]),rd.choice([0,2]),rd.choice([0,2]),rd.choice([0,2]),1],
              [1,rd.choice([0,2]),rd.choice([0,2]),rd.choice([0,2]),rd.choice([0,2]),1],
              [1,rd.choice([0,2]),rd.choice([0,2]),rd.choice([0,2]),rd.choice([0,2]),1],
              [1,1,1,1,1,1]]
    return matrix;

def funcaoMapear(): # funcaoMapear
    funcaoMapear = [[1,1,4],
                    [2,1,4],
                    [3,1,4],
                    [4,1,2],
                    [4,2,3],
                    [3,2,3],
                    [2,2,2],
                    [2,3,4],
                    [3,3,4],
                    [4,3,2],
                    [4,4,3],
                    [3,4,3],
                    [2,4,3],
                    [1,4,1],
                    [1,3,1],
                    [1,2,1]]
    return funcaoMapear

def estadoAtual(matrix,posicao): # retorna o estado atual na posicao informada
    return matrix[posicao[1]][posicao[0]]

def agenteObjetivo(matrix,percepcao,objObtido):

    if(objObtido == 0): # se objetivo foi alcançado
        return 6 #parar
    
    posicao = percepcao[0] #posicao atual
    estado = estadoAtual(matrix,posicao) #estado atual
    posicaoObj = encontrarSujeiraMenorDistancia(matrix,percepcao[0]) #posicao Objetivo

    if(estado == 2): #se estiver sujo
        print('estado: '+str(estado)+' acao: aspirar')
        return 'aspirar'    
    if(posicao[1] < posicaoObj[0]): #andar abaixo
        print('estado: '+str(estado)+' acao: abaixo')
        return 'abaixo'
    elif(posicao[1] > posicaoObj[0]): #andar acima
        print('estado: '+str(estado)+' acao: acima')
        return 'acima'
    if(posicao[0] < posicaoObj[1]): #andar direita
        print('estado: '+str(estado)+' acao: direita')
        return 'direita'
    elif(posicao[0]>posicaoObj[1]): #andar esquerda
        print('estado: '+str(estado)+' acao: esquerda')
        return 'esquerda'
    
def checkObj(matrix):
    for s in matrix:
        for n in s:
            if(n == 2):
                return 1
    return 0

#procura a sujeira mais proxima do robo
def encontrarSujeiraMenorDistancia(matrix,posicao):
    if(estadoAtual(matrix,posicao)==2): #caso esteja sujo retorna a posicao atual
        return posicao
    menorDistancia = 99999 #inicializa variavel de menor distancia
    posicaoSujeira = posicao #inicializa posicaoSujeira
    nlinha = 0 #contador de linha
    for linha in matrix:
        ncasa = 0 #contador de casa
        for casa in linha:
            #if casa estiver suja
            if(casa == 2):
                sujeira = [nlinha,ncasa] #posica da sujeira

                distancia = calcularDistancia(posicao,sujeira) #distancia até sujeira
                if(distancia < menorDistancia): #compara para encontrar a menor distancia, caso seja menor salva a posicao
                   menorDistancia = distancia 
                   posicaoSujeira = sujeira
            ncasa +=1                   
        nlinha +=1
    return posicaoSujeira

def calcularDistancia(posicaoAtual,posicaoSujeira): #retorna a distancia da posicao atual até a posicao da sujeira
    cont = 0 # contador de distancia
    x = posicaoAtual[0] #posicao atual
    y = posicaoAtual[1]
    xObj = posicaoSujeira[1] #posicao objetivo
    yObj = posicaoSujeira[0]
    cont += distanciaReta(y, yObj)
    cont += distanciaReta(x, xObj)
    return cont

def distanciaReta(pos, obj): #distancia entre dois pontos linha ou coluna
    i = 0
    while pos != obj: 
        if pos > obj:
            pos -= 1
            i+=1
        else:
            pos +=1
            i+=1
    return i
    

#move o robo baseado na acao informada                
def executarAcao(matrix,percepcao,acao):
    posicao = percepcao[0] #pega posicao do robo
    estado = percepcao[1]  #pega o estado atual
    
    #if para verificar a acao, mudar a posicao do robo e verificar o estado
    if acao =='acima':
        posicao = [posicao[0],posicao[1]-1]
        estado = estadoAtual(matrix,posicao)
    elif acao =='abaixo':
        posicao = [posicao[0],posicao[1]+1]
        estado = estadoAtual(matrix,posicao)
    elif acao =='esquerda':
        posicao = [posicao[0]-1,posicao[1]]
        estado = estadoAtual(matrix,posicao)
    elif acao =='direita':
        posicao = [posicao[0]+1,posicao[1]]
        estado = estadoAtual(matrix,posicao)
    elif acao =='aspirar':
        matrix[posicao[1]][posicao[0]] = 0
        estado = estadoAtual(matrix,posicao)
    
    percepcao = [posicao,estado] #salva as informações na percepcao
    return percepcao #retorna a nova a percepcao com a nova posicao e estado do robo

def agenteReativoSimples(matrix,mapa,percepcao): # retorna a acao que o robo deve tomar
    posicao = percepcao[0] #pega posicao robo
    estado = estadoAtual(matrix,posicao) #pega estado robo
    if(estado == 2): #verifica estado
        return 'aspirar'
    else:
        for a in mapa: #procura a acao que o robo deve tomar
            if(a[0] == posicao[0]) and (a[1] == posicao[1]):
                if a[2] == 1:
                    return 'acima'
                elif a[2] == 2:
                    return 'abaixo'
                elif a[2] == 3:
                    return 'esquerda'
                elif a[2] == 4:
                    return 'direita' 
main()

#Amanda Miranda Zanella, Bárbara Alessandra Maas, Bruno Henrique Wiedemann Reis e Lucas Miguel Vieira

#A sua solução é extensível para um mundo 3 x 3? E para um mundo 6 x 6? Explique sua resposta.
#Não a solução foi criada pensando em um mundo 4x4, seria possivel adaptar a solução para outros mundos alterando a funcão mapear, que é a 
#responsavel por definir o caminho pelo qual o robo deve seguir.

#É possível ter todo o espaço limpo efetivamente? Justifique sua resposta.
#Sim, a cada acao é verificado o estado do ambiente e a posicao da sujeira, portanto ele saberá se tem ou não sujeira e aonde ela está, e só
#vai parar até que todo o ambiente esteja limpo