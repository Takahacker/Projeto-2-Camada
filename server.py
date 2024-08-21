import struct
from enlace import *
import time
import numpy as np
from IEE754_Converter import IEE754_Converter  # Importa a classe de conversão

#Mudar de acordo com a entrada
serialName = "/dev/cu.usbmodem101"                  

def main():
    try:
        print("Iniciou o main")
        com1 = enlace(serialName)
        com1.enable()
        print("Abriu a comunicação")
        
        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)
        
        numeros_recebidos = []
        converter = IEE754_Converter()
        print("Okaaay lets go 🏎️ 🏁")
        time.sleep(2)
        print("a espera acabou 🕰️")
        
        start_time = time.time()  # Inicia o contador de tempo
        while True:
            rxBuffer, nRx = com1.getData(4) 
            if nRx > 0:
                print("Recebeu {} bytes".format(nRx))
                # Converte o buffer de bytes para string binária
                numero = struct.unpack('>f', rxBuffer)  # Remova a decodificação para string
                print("Mensagem recebida:", numero)
                numeros_recebidos.append(numero)
                print("número armazenado")
                print("números recebidos:", numeros_recebidos)
                
                start_time = time.time()  # Reinicia o contador após receber dados

            else:
                print("Nenhum dado recebido.")
                # Verifica se passou 1 minuto
                if time.time() - start_time > 60:
                    print("Timeout: mais de 1 minuto sem receber dados.")
                    break
                time.sleep(0.5)  # Aguarda meio segundo antes de tentar receber novamente

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

    finally:
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()

if __name__ == "__main__":
    main()