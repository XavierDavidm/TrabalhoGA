
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
        self.carregaDados() #inclui deserialização integral

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

        #arquivo de reserva.txt para reservas(matriz)
        with open('reserva.txt','r') as ARQreservas:
            nLinhas=int(sum(1 for _ in ARQreservas))
            ARQreservas.seek(0)
            reservas = []
            for i in range(nLinhas):
                linha = ARQreservas.readline().strip()
                a=linha.split(',',4)
                #atributos->,quarto(Quarto),int(diaInicio),int(diaFim),string(cliente),char(status(A/C/I/O))
                reserva=Reserva(a[0],a[1],a[2],a[3],a[4]) #cria o objeto reserva
                reservas.append(reserva) #coloca cada reserva(linha) em uma matriz(reservas)
                self.reservas=reservas
        
        #arquivo de produtos.txt para produtos(matriz)
        with open('produto.txt', 'r') as ARQprodutos:
            nLinhas = int(sum(1 for _ in ARQprodutos))
            ARQprodutos.seek(0)
            produtos = []
            for i in range(nLinhas):
                linha = ARQprodutos.readline().strip()
                a = linha.split(',', 3)
                produto = Produto(a[0].strip(), a[1].strip(), float(a[2].strip()))  # Remover espaços
                produtos.append(produto)
            self.produtos=produtos
        
        return {
            "quartos": self.quartos,
            "reservas": self.reservas,
            "produtos": self.produtos
        }

    def salvaDados(self):
        #filtra apenas reservas ativas e em check-in para serem salvas
        reservas_validas=[reserva for reserva in self.reservas if reserva.status in ['A', 'I']]
        #quartos
        with open('quarto.txt', 'w') as f:
            for quarto in self.quartos:
                f.write(f"{quarto.numero},{quarto.categoria},{quarto.diaria},{','.join(quarto.consumo)}\n")
        #reservas validas
        with open('reserva.txt', 'w') as f:
            for reserva in reservas_validas:
                f.write(f"{reserva.quarto},{reserva.diaInicio},{reserva.diaFim},{reserva.cliente},{reserva.status}\n")
        #produtos
        with open('produto.txt', 'w') as f:
            for produto in self.produtos:
                f.write(f"{produto.codigo},{produto.nome},{produto.preco}\n")
        print("Dados salvos com sucesso!")

    def consultaDisponibilidade(self, data, numero_quarto): 
        for quarto in self.quartos:
            if quarto.numero == numero_quarto:
                # Verifica se a data está entre diaInicio e diaFim de qualquer reserva
                for reserva in self.reservas:
                    if reserva.quarto == quarto.numero and reserva.diaInicio <= data <= reserva.diaFim:
                        print('O quarto escolhido já está ocupado!')
                        return
                print('O quarto escolhido está disponível!')
                print('Informações do quarto:')
                print(f"Número: {quarto.numero}")
                print(f"Categoria: {self.tipos_categorias.get(quarto.categoria, 'Desconhecido')}") 
                print(f"Diária: {quarto.diaria}")
                return
        raise ValueError("Quarto inválido.")

    def consultaReserva(self, data=None, cliente=None, numero_quarto=None):
        reservas_encontradas = []
        #sistema de validação de reserva, primeiro verifica Ativas
        for reserva in self.reservas:
            if reserva.status != 'A':
                continue  
            #filtro de nome do cliente,data e quarto
            cliente_ok = (cliente is None or cliente.strip() == '' or reserva.cliente.lower() == cliente.lower())
            data_ok = (data is None or (reserva.diaInicio <= data <= reserva.diaFim))
            quarto_ok = (numero_quarto is None or reserva.quarto == numero_quarto)
            #baseado nos campos digitados seram adicionados as reservas compativeis(lista)
            if data_ok and cliente_ok and quarto_ok:
                reservas_encontradas.append(reserva)
        #sistema de print caso encontre a reserva correspondente ao filtro
        if reservas_encontradas:
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
                
        else:
            print("Nenhuma reserva encontrada com os dados informados.")

    def realizarReserva(self,dataI,dataF,cliente,numero_quarto):
        #filtro disponivilidade quarto
        for reserva in self.reservas:
            if reserva.quarto == numero_quarto and \
            (reserva.diaInicio <= dataF and reserva.diaFim >= dataI):
                print("O quarto já está reservado para esse período.")
                return

        #filtra reserva ativa ou em check-in
        for reserva in self.reservas:
            if reserva.cliente.lower() == cliente.lower() and \
            reserva.status in ['A', 'I']:  # 'A' = Ativa, 'I' = Check-In
                print("O cliente já possui uma reserva ativa ou em check-in.")
                return

        #se passar nos filtros cria reserva e adiciona ao reservas(matriz)
        nova_reserva = Reserva(numero_quarto, dataI, dataF, cliente, 'A')  # 'A' = Ativa
        self.reservas.append(nova_reserva)
        print("Reserva realizada com sucesso!")

    def cancelaReserva(self, cliente):
        #procura até encontrar a reserva ativa no nome do cliente
        #caso contrario retorna que não ha reserva ativa
        reserva_encontrada = False
        for reserva in self.reservas:
            if reserva.cliente.lower() == cliente.lower() and reserva.status == 'A':
                reserva.status = 'C'  # 'C' = Cancelada
                reserva_encontrada = True
                print(f"Reserva do cliente '{cliente}' foi cancelada com sucesso!")
                break
        if not reserva_encontrada:
            print("Nenhuma reserva ativa encontrada no Nome informado.")

    def realizaCheckIn(self,cliente):
        #filtro se existe a reserva(semelhante ao cancela reserva)
        reserva_encontrada = False
        for reserva in self.reservas:
            if reserva.cliente.lower() == cliente.lower() and reserva.status == 'A':
                reserva.status = 'I'  # 'I' = check-In
                reserva_encontrada = True
                #print dos dados
                print(f"Data Inicial: {reserva.diaInicio}")
                print(f"Data Final: {reserva.diaFim}")
                TotalDias=reserva.diaFim-reserva.diaInicio
                print(F"Quantidade de Dias: {TotalDias}")
                quarto = next((q for q in self.quartos if q.numero == reserva.quarto), None)
                TotalDiarias=TotalDias*quarto.diaria
                print(F"VALOR Total das Diarias: {TotalDiarias}")
                if quarto:
                    print('Informações do quarto:')
                    print(f"Número: {quarto.numero}")
                    print(f"Categoria: {self.tipos_categorias.get(quarto.categoria, 'Desconhecido')}") 
                    print(f"Diária: {quarto.diaria}")
                    print('Check-In realizado com sucesso! aproveite sua estadia!')
                return  
        if not reserva_encontrada:
            print("Nenhuma reserva ativa encontrada no Nome informado.")

    def realizaCheckOut(self, cliente):
        reserva_encontrada = False
        
        for reserva in self.reservas:
            if reserva.cliente.lower() == cliente.lower() and reserva.status == 'I':
                reserva_encontrada = True
                quarto = next((q for q in self.quartos if q.numero == reserva.quarto), None)
                
                if quarto:
                    #calculos
                    total_dias = reserva.diaFim - reserva.diaInicio
                    total_diarias = total_dias * quarto.diaria
                    total_consumo = quarto.valorTotalConsumo(pousada.produtos)
                    valor_final = total_diarias + total_consumo
                    #prints
                    print(f"Cliente: {reserva.cliente}")
                    print(f"Data Inicial: {reserva.diaInicio}")
                    print(f"Data Final: {reserva.diaFim}")
                    print(f"Quantidade de Dias: {total_dias}")
                    print(f"Valor Total das Diárias: R${total_diarias:.2f}")
                    #prints dos consumos
                    quarto.listaConsumo(pousada.produtos)
                    print(f"Valor Total dos Consumos: R${total_consumo:.2f}")
                    print(f"Valor Final a ser Pago: R${valor_final:.2f}")
                    #check-out
                    reserva.status = 'O'  # 'O' = check-out
                    #limpeza
                    quarto.limpaConsumo()
                    print("Check-out realizado com sucesso!")
        if not reserva_encontrada:
            print("Nenhuma reserva em check-in encontrada para o cliente informado.")

    def registrarConsumo(self, cliente):
        #validação check-in do cliente informado
        reserva_encontrada = None
        for reserva in self.reservas:
            if reserva.cliente.lower() == cliente.lower() and reserva.status == 'I':
                reserva_encontrada = reserva
                break
        if not reserva_encontrada:
            print("Nenhuma reserva em check-in encontrada para o cliente informado.")
            return
        #print dos produtos disponíveis
        print("Produtos disponíveis na copa:")
        for produto in self.produtos:
            print(f"Código: {produto.codigo}, Nome: {produto.nome}, Preço: R${produto.preco:.2f}")
        #input do codigo
        codigo_produto = input("Digite o código do produto desejado: ")
        codigo_limpo = codigo_produto.strip() 
        #validaçao de produto
        produto_encontrado = next((p for p in self.produtos if p.codigo == int(codigo_limpo)), None)
        if produto_encontrado:
            quarto = next((q for q in self.quartos if q.numero == reserva_encontrada.quarto), None)
            if quarto:
                # Adiciona o consumo usando o método da classe Quarto
                quarto.adicionaConsumo(codigo_limpo)  # Adiciona o código do produto à lista de consumo
                print(f"Consumo registrado: {produto_encontrado.nome} - R${produto_encontrado.preco:.2f}")
            else:
                print("Quarto não encontrado.")
        else:
            print("Produto não encontrado.")

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

    def adicionaConsumo(self, codigo_produto):
        self.consumo.append(codigo_produto)

    def listaConsumo(self, produtos):
        if not self.consumo:
            print("Não há consumo registrado para este quarto.")
            return
        print("Consumo do Quarto", self.numero, ":")
        for codigo in self.consumo:
            codigo_limpo = codigo.strip('() ') #limpeza de caracteres
            try:
                produto = next((p for p in produtos if p.codigo == int(codigo_limpo)), None)
                if produto:
                    print(f"Produto: {produto.nome}, Preço: R${produto.preco:.2f}")
                else:
                    print(f"Produto com código {codigo_limpo} não encontrado.")
            except ValueError:
                print(f"Código de produto inválido: {codigo}.")

    def valorTotalConsumo(self, produtos):
        total = 0.0
        for codigo in self.consumo:
            #para garantir que será int e não havera nenhum espaço ou ' e ()
            codigo_limpo = codigo.strip('() ')  
            produto = next((p for p in produtos if p.codigo == int(codigo_limpo)), None)
            if produto:
                total += produto.preco
        return total
    
    def limpaConsumo(self):
        #Limpa a lista de consumo
        self.consumo = []

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
        print("---------------------------")
        sair=True
        pousada.salvaDados()
        print('Encerrando Sistema...')
        print("---------------------------")

    elif resposta == 1:
        print("---------------------------")
        data=int(input('digite a data que deseja consultar: '))
        numero_quarto=int(input('digite o número do quarto que deseja consultar: '))
        print("---------------------------")
        pousada.consultaDisponibilidade(data,numero_quarto)
        print("---------------------------")

    elif resposta == 2:
        print("---------------------------")
        data_input = input('Digite a data que deseja consultar (ou pressione Enter para pular): ')
        cliente = input('Digite o nome do cliente (ou pressione Enter para pular): ')
        numero_quarto_input = input('Digite o número do quarto (ou pressione Enter para pular): ')
        data = int(data_input) if data_input else None
        numero_quarto = int(numero_quarto_input) if numero_quarto_input else None
        print("---------------------------")
        pousada.consultaReserva(data, cliente, numero_quarto)
        print("---------------------------")
        
    elif resposta == 3:
        print("---------------------------")
        dataI=int(input('digite a data inicial da sua reserva: '))
        dataF=int(input('digite a data do fim da sua reserva: '))
        cliente=str(input('digite seu nome para reserva: '))
        numero_quarto=int(input('digite o número do quarto que deseja reservar: '))
        print("---------------------------")
        pousada.realizarReserva(dataI,dataF,cliente,numero_quarto)
        print("---------------------------")

    elif resposta == 4:
        print("---------------------------")
        cliente=str(input('digite o nome em que a reserva está registrada para cancelar: '))
        print("---------------------------")
        pousada.cancelaReserva(cliente)
        print("---------------------------")

    elif resposta == 5:
        print("---------------------------")
        cliente=str(input('digite o nome de quem é a reserva: '))
        print("---------------------------")
        pousada.realizaCheckIn(cliente)
        print("---------------------------")

    elif resposta == 6:
        print("---------------------------")
        cliente=str(input('digite o nome de quem é a reserva: '))
        print("---------------------------")
        pousada.realizaCheckOut(cliente)
        print("---------------------------")

    elif resposta == 7:
        print("---------------------------")
        cliente=str(input('digite o nome de quem é a reserva: '))
        print("---------------------------")
        pousada.registrarConsumo(cliente)
        print("---------------------------")

    elif resposta == 8:
        pousada.salvaDados()
