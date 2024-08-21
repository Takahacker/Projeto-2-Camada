import struct
from enlace import *
import time
import numpy as np
from IEE754_Converter import IEE754_Converter  # Importa a classe de conversão

serialName = "COM7"  # Nome da porta de comunicação

def main():
    try:
        print("Iniciou o main")
        com1 = enlace(serialName)
        com1.enable()
        print("Abriu a comunicação")
        time.sleep(.2)
        com1.sendData(b'00')
        print("byte de sacrfifício enviado")
        time.sleep(1)

        # Lê os números do arquivo listaEnvio.txt com codificação UTF-8
        with open('listaEnvio.txt', 'r', encoding='utf-8') as file:
            numeros = file.readlines()

        for numero in numeros:
            numero = numero.strip()
            try:
                numero_float = float(numero)  # Converte a string para float
                ieee754_bytes = struct.pack('>f', numero_float)  # Converte para IEEE 754 em formato binário (big-endian float)
                print(f"Enviando: {ieee754_bytes.hex()}")  # Exibe os bytes em formato hexadecimal para visualização
                time.sleep(0.5)
                com1.sendData(ieee754_bytes)  # Envia os bytes diretamente
                print("Número enviado")
                
                while com1.tx.threadMutex == True:
                    time.sleep(0.01)
                txSize = com1.tx.getStatus()
                print(f'Enviou = {txSize}')
            except ValueError as ve:
                print(f"Erro ao converter '{numero}' para float: {ve}")
                continue  # Pula para o próximo número

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

if __name__ == "__main__":
    main()