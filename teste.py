class Pousada:
    def __init__(self) -> None:
        pass

class Reserva:
    def __init__(self) -> None:
        pass

class Quarto:
    def __init__(self) -> None:
        pass

class Produto:
    def __init__(self) -> None:
        pass

#chamar uma função que cria pousada se não existir e da load em uma existente (arquivo)
#main menu
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

arquivo=open('pousada.txt','w')
arquivo=open('quarto.txt','w')
arquivo=open('reserva.txt','w')
arquivo=open('produto.txt','w')