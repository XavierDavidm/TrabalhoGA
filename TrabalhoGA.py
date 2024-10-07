
#OBSERVAÇÃO->por todo o codigo se encontram explicações das funções,metodos e atributos

import os

class Pousada:
    def __init__(self): #atributos-> str(nome),str(contato),quartos-lista,reservas-lista,produtos-lista
        #set dos atributos (serão substituidos pelos dados das funções que carregam os arquivos)
        self.__nome=0
        self.__contato=0
        self.quartos=0
        self.reservas=0
        self.produtos=0
        self.carregaDados()   


    #função especial para verificar se um arquivo existe ou não, será usada para garantir que os arquivos txt serão gerados se não existirem
    def verificarArquivo(self,nomeArquivo):
        return os.path.isfile(nomeArquivo)

    #atributo nome 
    @property
    def nome(self):
        return self.__nome
    @nome.setter
    def nome(self):
        raise ValueError('erro nome pousada')
    #usado somente se não existir nome da pousada no pousada.txt
    def registarNome(self):
        nome=str(input('digite o nome da pousada: '))
        self.__nome=nome
    def getNome(self):
        return self.__nome
    
    #atributo contato 
    @property
    def contato(self):
        return self.__contato
    @contato.setter
    def contato(self):
        raise ValueError('erro contato pousada')
    #usado somente se não existir contato no pousada.txt
    def registrarContato(self):
        contato=str(input('digite o contato da pousada'))
        self.__contato=contato
    def getContato(self):
        return self.__contato

    #metodos da pousada
    def carregaDados(self):
        #carrega os dados dos arquivos de texto

        #arquivo de quartos.txt para quarto(matriz)
        ARQquartos=open('quarto.txt','r')
        nLinhas=ARQquartos.readline()
        quartos=[]
        for i in range(nLinhas):
            a=ARQquartos.readline()
            a=a.split(1,1)
            #ordem->numero,status,diaria,lista com codigos dos produtos
            quarto=Quarto(a[0],a[1],a[2],a[3]) 
            quartos.append(quarto)
        ARQquartos.close()
        return quartos

    def salvaDados(self):
        pass

    def consultaDisponibilidade(self,data,quarto): #quarto se refere ao quarto escolhido pelo cliente atraves de input
        pass

    def consultaReserva(self,cliente,quarto):
        pass

    def realizarReserva(datas,clitente,quarto):
        pass

    def cancelaReserva(cliente):
        pass

    def realizaCheckIn(cliente):
        pass

    def realizaCheckOut(cliente):
        pass

class Quarto: #atributos->int(numero),char(categoria(s/m/p),float(diaria),int(consumo(lista)))
    def __init__(self,numero,status,diaria,consumo): 
        self.numero=int(numero)
        self.status=str(status)
        self.diaria=float(diaria)
        self.consumo=int(consumo())
        
    def adicionaConsumo():
        pass
    def listaConsumo():
        pass
    def valorTotalConsumo():
        pass
    def limpaConsumo():
        pass

class Reserva:   #atributos->int(diaInicio),int(diaFim),string(cliente),quarto(Quarto),char(status(A/C/I/O))
    def __init__(self):
        pass

class Produto: #atributos->int(codigo),str(nome),float(preco)
    def __init__(self):
        pass

#chamar uma função que cria pousada se não existir e da load em uma existente (arquivo)
#main menu
#ANOTAÇÃO
#SERIALIZAR==CLASSE-->STRING usar quando for salvar e precisar transformar todos os objetos para string na planilha
#DESERIALIZAR==STRING-->CLASSE usar quando tiver as strings carregadas e transformar em objeto


sair=False
while sair!=True:
    print('seja bem-vindo!')
    print('----- MENU -----')
    print('1 -> Consultar disponibilidade')
    print('2 -> Consultar reserva')
    print('3 -> Realizar reserva')
    print('4 -> Cancelar reserva')
    print('5 -> Realizar check-in')
    print('6 -> Realizar check-out')
    print('7 -> Registrar consumo')
    print('8 -> Salvar')
    print('0 -> Sair')
    resposta=int(input('Selecione a opção que deseja realizar: '))
    if resposta == 0:
        sair=True
        #chamar o save aqui antes de sair
        print('Encerrando Sistema...')
    elif resposta ==1:
        pass
    elif resposta ==2:
        pass
    elif resposta ==3:
        pass
    elif resposta ==4:
        pass
    elif resposta ==5:
        pass
    elif resposta ==6:
        pass
    elif resposta ==7:
        pass
    elif resposta ==8:
        pass

