freeSpc = int(input("Memoria total: "))
blockTam = int(input("Tamanho do Bloco: "))

def interface(dir):
    global freeSpc
    while(True):
        print(f"Diretorio atual:  {dir.nomedir} \n" )
        print(dir.blocklist)
        print(int(freeSpc/blockTam))
        print("1- Criar arquivo\n2- Criar diretorio\n3- Acessar diretorio\n4- Deletar arquivo\n5- Deletar Diretorio\n6- Sair\n")
        inp = int(input(":"))
        if inp == 1:    #Criar arq
            nome = input("Nome do arquivo: ")
            existe = False
            for x in dir.blocklist:
                if x == nome:
                    existe = True

            if existe == False:
                dir.addarq(nome, int(input("Tamanho do arquivo em MB: ")))
                print(dir.blocklist)
            else:
                print("Arquivo ja existe")
            #tamMax
        elif inp == 2:  #Criar Dir
                freeSpc -= blockTam
                nome = input("Nome do diretorio: ")
                existe = False
                for x in dir.blocklist:
                    if x == nome:
                        existe = True
                if existe == False:
                    dir.addDir(nome)
                    print(dir.blocklist)
                else:
                    print("Diretorio ja existe")
        elif inp == 3:  #Acessar Dir
            nome = input("Digite o nome do diretorio a acessar: ")
            for i,x in enumerate(dir.blocklist):
                if type(dir.blocklist[i]) != str and dir.accessdir(dir.blocklist[i], nome):
                    interface(dir.blocklist[i])
        elif inp == 4:  #Deletar Arq
            delet = input("Nome do arquivo a ser deletado: ")
            achou = False
            for i,x in enumerate(dir.blocklist):
                if x == delet:
                    dir.blocklist[i] = "Livre"
                    freeSpc += blockTam
                    achou == True
        
            if achou == False:
                print("Arquivo nao existe")

            print(dir.blocklist)
        elif inp == 5:  #Deletar Dir
            nome = input("Digite o nome do diretorio a deletar: ")
            for i,x in enumerate(dir.blocklist):
                if type(dir.blocklist[i]) != str and dir.accessdir(dir.blocklist[i], nome):
                    dir.deletDir(dir.blocklist[i])
                    dir.blocklist[i] = "Livre"
                    freeSpc += blockTam
            
        elif inp == 6:  #Back
            # ocupado = 0
            # for i,x in enumerate(dir.blocklist):
            #     if dir.blocklist[i] != "Livre":
            #         ocupado += blockTam

            # # freeSpc += ocupado
            break


class memoriaDir:
    def __init__(self, nomedir):
            self.nomedir = nomedir
            self.blocklist = []
            for x in range (int(freeSpc/blockTam)):
                self.blocklist.append("Livre")
            
    def addarq(self, nome, tam):
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
        
    def addDir(self, nome):
        m2 = memoriaDir(nome)
        for i,x in enumerate(self.blocklist):
            if x == "Livre":
                self.blocklist[i] = m2
                break


    def accessdir(self, dir, nome):
            if dir.nomedir == nome:
                return True

    def deletDir(self, dir):
        global freeSpc
        ocupado = 0
        for i,x in enumerate(dir.blocklist):
            if x != "Livre":
                dir.blocklist[i] = "Livre"
                ocupado += blockTam
        freeSpc += ocupado
                
        


m1 = memoriaDir(input("Nome da unidade de memoria ou diretorio: "))
interface(m1)
