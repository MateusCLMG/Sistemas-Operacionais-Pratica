freeSpc = int(input("Memoria total: "))
blockTam = int(input("Tamanho do Bloco: "))

class memoriaDir:
    def __init__(self, nomedir):
            self.nomedir = nomedir
            self.blocklist = []
            for x in range (int(freeSpc/blockTam)):
                self.blocklist.append("Livre")
            
    def addarq(self, nome, tam):    #Mesmo metodo para alocação de memoria
        global freeSpc
        print(f"{nome} tem {tam} MBs\n")
        counter = 0 
        memoriaLivre = 0

        for x in self.blocklist:
            if x == "Livre":
                 memoriaLivre += blockTam

        while tam > 0 and counter < len(self.blocklist):
           
           
            if tam > memoriaLivre:
                print(f"{nome} nao pode ser alocado na memoria virtual!\n")
                break
            
            if self.blocklist[counter] == "Livre":
                tam -= blockTam
                freeSpc -= blockTam  #!!!
                print(f"{nome} ocupou o bloco {counter}\n")
                self.blocklist[counter] = nome
                if tam < 0:
                    print(f"Houve fragmentacao interna de {abs(tam)} MBs  no bloco {counter}\n")
                else:
                    print(f"Nao houve fragmentacao interna nos blocos \n")
            counter += 1
        
    def addDir(self, nome):     #Cria um outro objeto memoriaDir no primeiro espaço livre
        m2 = memoriaDir(nome)
        for i,x in enumerate(self.blocklist):
            if x == "Livre":
                self.blocklist[i] = m2
                break
    def checkNameDir(self, dir, nome):  #Compara o nome de uma entrada do usuario com o nome de um diretorio
        if dir.nomedir == nome:
            return True

    def accessdir(self, dir, nome):
            if dir.nomedir == nome:
                return True

    def deletDir(self, dir):    #conta a quantidade de espaço que os arquivos de um diretorio ocupam,
        global freeSpc          #deleta este diretorio, e retorna a memoria ocupada para a memoria principal
        ocupado = 0
        for i,x in enumerate(dir.blocklist):
            if x != "Livre":
                dir.blocklist[i] = "Livre"
                ocupado += blockTam
        freeSpc += ocupado

    def countDir(self, dir):    #conta a quantidade de espaço que o arquivo de um diretorio ocupa, para
        ocupado = blockTam      #printar essa quantidade na listagem
        for i,x in enumerate(dir.blocklist):
            if dir.blocklist[i] != "Livre":
                ocupado += blockTam

        return (dir.nomedir, ocupado)

def interface(dir):
    global freeSpc
    while(True):
        print(f"Diretorio atual:  {dir.nomedir} \n" )

        print(dir.blocklist)
        print(f"Quantidade de blocos livre: {int(freeSpc/blockTam)}")
        print("1- Criar arquivo\n2- Criar diretorio\n3- Acessar diretorio\n4- Deletar arquivo\n5- Deletar Diretorio\n6- Listar conteudo\n7- Sair\n")
        inp = int(input(":"))
        if inp == 1:    #Criar arq
            nome = input("Nome do arquivo: ")
            existe = False
            for x in dir.blocklist: #verifica se ja existe arquivo com este nome
                if x == nome:
                    existe = True

            if existe == False:
                dir.addarq(nome, int(input("Tamanho do arquivo em MB: ")))
            else:
                print("Arquivo ja existe")
            #tamMax
        elif inp == 2:  #Criar Dir
            freeSpc -= blockTam
            nome = input("Nome do diretorio: ")
            existe = False
            for x in dir.blocklist: #verifica se ja existe arquivo com este nome
                if x == nome:
                    existe = True

            for i,x in enumerate(dir.blocklist):    #verifica se ja existe diretorio com este nome
                if type(dir.blocklist[i]) != str and dir.checkNameDir(dir.blocklist[i], nome):
                    existe == True
                
            if existe == False:
                dir.addDir(nome)
            else:
                print("Nome ja existe")
        elif inp == 3:  #Acessar Dir
            nome = input("Digite o nome do diretorio a acessar: ")  
            for i,x in enumerate(dir.blocklist):    #procura um diretorio com o nome dado como input pelo usuario
                if type(dir.blocklist[i]) != str and dir.accessdir(dir.blocklist[i], nome):
                    interface(dir.blocklist[i])     #e instancia uma nova interface() dentro deste diretorio
        elif inp == 4:  #Deletar Arq
            delet = input("Nome do arquivo a ser deletado: ")
            achou = False
            for i,x in enumerate(dir.blocklist):    #procura por todos os blocos com o nome de arquivo dado pelo usuario
                if x == delet:
                    dir.blocklist[i] = "Livre"
                    freeSpc += blockTam             #e libera a memoria ocupada
                    achou == True
        
            if achou == False:
                print("Arquivo nao existe")

        elif inp == 5:  #Deletar Dir
            nome = input("Digite o nome do diretorio a deletar: ")
            for i,x in enumerate(dir.blocklist):    #Procura por objetos MemoriaDir dentro da lista de blocos com o nome dado como entrada
                if type(dir.blocklist[i]) != str and dir.accessdir(dir.blocklist[i], nome):
                    dir.deletDir(dir.blocklist[i])
                    dir.blocklist[i] = "Livre"      #deleta e libera a memoria ocupada
                    freeSpc += blockTam
        elif inp ==6:   #Listar
            print("Arquivos:\n")
            listagem = []
            for i,x in enumerate(dir.blocklist):    #Conta as repetições de cada elemento da lista (isso é equivalente ao seu tamanho), e os
                if type(dir.blocklist[i]) == str and dir.blocklist[i] != "Livre" and dir.blocklist[i] != dir.blocklist[i-1]:    #nomes dos elementos
                    listagem.append((dir.blocklist[i], dir.blocklist.count(x) * blockTam))                                      #sem se repetir
            print(listagem)
            print("Diretorios: \n")                 
            listagemDir = []
            for i,x in enumerate(dir.blocklist):
                if type(dir.blocklist[i]) != str:
                    listagemDir.extend(dir.countDir(dir.blocklist[i]))  #Acessa o diretorio e realiza outra contagem dos elementos dentro dele
                                                                        #para retornar a memoria ocupada
            print(listagemDir)
            
        elif inp == 7:  #Back
            break   #quebra o loop da interface atual. Finaliza o programa se estiver na raiz





        


m1 = memoriaDir(input("Nome da unidade de memoria ou diretorio: "))
interface(m1)
print("\nFIM")