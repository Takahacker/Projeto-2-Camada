from enlace import *
import time
import numpy as np
from IEE754_Converter import IEE754_Converter  # Importa a classe de conversão

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "/dev/cu.usbmodem2101"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")

        # Lê os números do arquivo listaEnvio.txt
        with open('listaEnvio.txt', 'r') as file:
            numeros = file.readlines()

        converter = IEE754_Converter()
        for numero in numeros:
            numero_float = float(numero.strip())  # Converte a string para float
            ieee754 = converter.converter_para_ieee754(numero_float)  # Converte para IEEE 754
            print(f"Enviando: {ieee754}")
            time.sleep(0.5)
            com1.sendData(ieee754)
            print("numero enviado")  # Envia os dados convertidos
            while com1.tx.threadMutex == True:
                time.sleep(0.01)
            txSize = com1.tx.getStatus()
            print('enviou = {}' .format(txSize))
        print("Todos os números foram enviados")

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()