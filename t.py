
#OBSERVAÇÃO->por todo o codigo se encontram explicações das funções,metodos e atributos

import os

class Pousada:
    def __init__(self): #atributos-> str(nome),str(contato),quartos-lista,reservas-lista,produtos-lista
        #set dos atributos (serão substituidos pelos dados das funções que carregam os arquivos)
        self.__nome=0
        self.__contato=0
        self.quartos = []  
        self.reservas = [] 
        self.produtos = []
        #dicionario para as categorias dos quartos
        self.tipos_categorias = { 
            'M': 'Master',
            'S': 'Standard',
            'P': 'Premium',
        }
        self.Status_Reservas = { 
            'A': 'Ativa',
            'C': 'Cancelada',
            'I': 'Check-In',
            'O': 'Check-Out',
        }
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
        contato=str(input('digite o contato da pousada: '))
        self.__contato=contato
    def getContato(self):
        return self.__contato

    #os outros atributos são carregados e/ou registrados pelos arquivos e funções especificas 

    #metodos da pousada
    def carregaDados(self):
        #carrega os dados dos arquivos de texto
        #arquivo pousada.txt para nome e contato da pousada
        #também verifica se o arquivo pousada.txt existe
        nomeArquivo='pousada.txt'
        if self.verificarArquivo(nomeArquivo)==True:
            with open('pousada.txt','r') as ARQpousada:
                nLinhas = int(ARQpousada.readline().strip())
                nLinhas = int(nLinhas)
                for i in range(nLinhas):
                    linha = ARQpousada.readline().strip()
                    a=linha.split(',',2)
                    self.__nome=a[0]
                    self.__contato=a[1]
        else:
            with open('pousada.txt','w') as ARQpousada:
                self.registarNome()
                self.registrarContato()
                ARQpousada.writelines('1')
                dados=(self.nome,',',self.contato)
                dados=str(dados)
                ARQpousada.writelines(dados)

        #arquivo de quartos.txt para quartos(matriz)
        with open('quarto.txt','r') as ARQquartos:
            nLinhas=int(sum(1 for _ in ARQquartos))
            ARQquartos.seek(0)
            quartos = []
            for i in range(nLinhas):
                linha = ARQquartos.readline().strip()
                a=linha.split(',',3)
                #ordem->numero,status,diaria,lista com codigos dos produtos
                quarto=Quarto(a[0],a[1],a[2],a[3]) #cria o objeto quarto
                quartos.append(quarto) #coloca cada quarto(linha) em uma matriz
            self.quartos=quartos
            print(self.quartos)

        #arquivo de reserva.txt para reservas(matriz)
        with open('reserva.txt','r') as ARQreservas:
            nLinhas=int(sum(1 for _ in ARQreservas))
            ARQreservas.seek(0)
            reservas = []
            for i in range(nLinhas):
                linha = ARQreservas.readline().strip()
                a=linha.split(',',4)
                #atributos->,quarto(Quarto),int(diaInicio),int(diaFim),string(cliente),char(status(A/C/I/O))
                print(f"Carregando reserva: {a}")
                reserva=Reserva(a[0],a[1],a[2],a[3],a[4]) #cria o objeto reserva
                reservas.append(reserva) #coloca cada reserva(linha) em uma matriz(reservas)
                self.reservas=reservas
            print(self.reservas)
        
        #arquivo de produtos.txt para produtos(matriz)
        with open('produto.txt','r') as ARQprodutos:
            nLinhas=int(sum(1 for _ in ARQprodutos))
            ARQprodutos.seek(0)
            produtos = []
            for i in range(nLinhas):
                linha = ARQprodutos.readline().strip()
                a=linha.split(',',3)
                produto=Produto(a[0],a[1],a[2])
                produtos.append(produto)
            self.produtos=produtos
            print(self.produtos)
        
        return {
            "quartos": self.quartos,
            "reservas": self.reservas,
            "produtos": self.produtos
        }

    def salvaDados(self):
        pass

    def consultaDisponibilidade(self, data, numero_quarto): 
        for quarto in self.quartos:
            if quarto.numero == numero_quarto:
                # Verifica se a data está entre diaInicio e diaFim de qualquer reserva
                for reserva in self.reservas:
                    if reserva.quarto == quarto.numero and reserva.diaInicio <= data <= reserva.diaFim:
                        print('O quarto escolhido já está ocupado!')
                        print("---------------------------")
                        return
                print('O quarto escolhido está disponível!')
                print('Informações do quarto:')
                print(f"Número: {quarto.numero}")
                print(f"Categoria: {self.tipos_categorias.get(quarto.categoria, 'Desconhecido')}") 
                print(f"Diária: {quarto.diaria}")
                print("---------------------------")
                return
        raise ValueError("Quarto inválido.")

    def consultaReserva(self, data=None, cliente=None, numero_quarto=None):
        reservas_encontradas = []

        for reserva in self.reservas:
            if reserva.status != 'A':
                continue  
            cliente_ok = (cliente is None or cliente.strip() == '' or reserva.cliente.lower() == cliente.lower())
            data_ok = (data is None or (reserva.diaInicio <= data <= reserva.diaFim))
            quarto_ok = (numero_quarto is None or reserva.quarto == numero_quarto)
            if data_ok and cliente_ok and quarto_ok:
                reservas_encontradas.append(reserva)

        if reservas_encontradas:
            print("---------------------------")
            print("Reservas encontradas:")
            for reserva in reservas_encontradas:
                print(f"Cliente: {reserva.cliente}")
                print(f"Data Inicial: {reserva.diaInicio}")
                print(f"Data Final: {reserva.diaFim}")
                quarto = next((q for q in self.quartos if q.numero == reserva.quarto), None)
                if quarto:
                    print('Informações do quarto:')
                    print(f"Número: {quarto.numero}")
                    print(f"Categoria: {self.tipos_categorias.get(quarto.categoria, 'Desconhecido')}") 
                    print(f"Diária: {quarto.diaria}")
                print("---------------------------")
        else:
            print("Nenhuma reserva encontrada com os dados informados.")


    def realizarReserva(datas,clitente,quarto):
        pass

    def cancelaReserva(cliente):
        pass

    def realizaCheckIn(cliente):
        pass

    def realizaCheckOut(cliente):
        pass

    def registrarConsumo(self):
        pass

class Quarto: #atributos->int(numero),char(categoria(s/m/p),float(diaria),int(consumo(lista)))
    def __init__(self,numero,categoria,diaria,consumo): 
        self.numero=int(numero)
        self.categoria=str(categoria)
        self.diaria=float(diaria)
        self.consumo = consumo.split(',')
        
    def __str__(self):
        return f"Quarto({self.numero},{self.categoria},{self.diaria},{self.consumo})"
    def __repr__(self):
        return self.__str__()

    def adicionaConsumo():
        pass

    def listaConsumo():
        pass

    def valorTotalConsumo():
        pass

    def limpaConsumo():
        pass

class Reserva:   #atributos->int(diaInicio),int(diaFim),string(cliente),quarto(Quarto),char(status(A/C/I/O))
    def __init__(self,quarto,diaInicio,diaFim,cliente,status):
        self.quarto=int(quarto)
        self.diaInicio=int(diaInicio)
        self.diaFim=int(diaFim)
        self.cliente=str(cliente)
        self.status=str(status)
    def __str__(self):
        return f"Reserva({self.quarto},{self.diaInicio},{self.diaFim},{self.cliente},{self.status})"
    def __repr__(self):
        return self.__str__()

class Produto: #atributos->int(codigo),str(nome),float(preco)
    def __init__(self,codigo,nome,preco):
        self.codigo=int(codigo)
        self.nome=str(nome)
        self.preco=float(preco)
    def __str__(self):
        return f"Produto({self.codigo},{self.nome},{self.preco})"
    def __repr__(self):
        return self.__str__()
    
#ANOTAÇÃO
#SERIALIZAR==CLASSE-->STRING usar quando for salvar e precisar transformar todos os objetos para string na planilha
#DESERIALIZAR==STRING-->CLASSE usar quando tiver as strings carregadas e transformar em objeto

#main menu
pousada=Pousada()
sair=False
print('Seja bem-vindo ao sistema da pousada',pousada.getNome(),'!')
while sair!=True:
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
        pousada.salvaDados()
        print('Dados Salvos com sucesso!')
        print('Encerrando Sistema...')

    elif resposta == 1:
        data=int(input('digite a data que deseja consultar'))
        numero_quarto=int(input('digite o número do quarto que deseja consultar: '))
        pousada.consultaDisponibilidade(data,numero_quarto)

    elif resposta == 2:
        data_input = input('Digite a data que deseja consultar (ou pressione Enter para pular): ')
        cliente = input('Digite o nome do cliente (ou pressione Enter para pular): ')
        numero_quarto_input = input('Digite o número do quarto (ou pressione Enter para pular): ')
        data = int(data_input) if data_input else None
        numero_quarto = int(numero_quarto_input) if numero_quarto_input else None
        pousada.consultaReserva(data, cliente, numero_quarto)
        
    elif resposta == 3:
        pousada.realizarReserva()
    elif resposta == 4:
        pousada.cancelaReserva()
    elif resposta == 5:
        pousada.realizaCheckIn()
    elif resposta == 6:
        pousada.realizaCheckOut()
    elif resposta == 7:
        pousada.registrarConsumo()
    elif resposta == 8:
        pousada.salvaDados()
        print('Dados Salvos com sucesso!')