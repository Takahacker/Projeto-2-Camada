import struct
from enlace import *
import time

serialName = "/dev/cu.usbmodem101"  # Mude conforme necessário

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
        print("Okaaay lets go 🏎️ 🏁")
        time.sleep(2)
        print("a espera acabou 🕰️")
        
        start_time = time.time()  # Inicia o contador de tempo
        timeout = 5  # Timeout de 5 segundos para indicar o fim da transmissão

        while True:
            # Verifica se há bytes disponíveis para leitura
            if com1.rx.getBufferLen() >= 4:  # Se há 4 ou mais bytes disponíveis no buffer
                rxBuffer, nRx = com1.getData(4)
                if nRx > 0:
                    numero = struct.unpack('>f', rxBuffer)[0]
                    print(f"Mensagem recebida: {numero}")
                    numeros_recebidos.append(numero)
                    print("número armazenado")
                    print("números recebidos:", numeros_recebidos)
                    
                    start_time = time.time()  # Reinicia o contador após receber dados
            else:
                # Verifica se passou o tempo limite sem receber dados
                if time.time() - start_time > timeout:
                    print("Timeout: mais de 5 segundos sem receber dados. Fim da transmissão.")
                    break
                time.sleep(0.5)  # Aguarda meio segundo antes de tentar ler novamente

    except Exception as erro:
        print("ops! :-\\")
        print(erro)

    finally:
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()

if __name__ == "__main__":
    main()