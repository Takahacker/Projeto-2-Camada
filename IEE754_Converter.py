import struct

class IEE754_Converter:

    def __init__(self):
        self.relevant_data = None

    def converter_para_ieee754(self, numero, bits=32):
        """
        Converte um número para a representação de ponto flutuante IEEE 754.

        Parâmetros:
        - numero: O número a ser convertido.
        - bits: O número de bits na representação IEEE 754. O padrão é 32.
        Retorna:
        - Um objeto bytes representando a representação IEEE 754 do número.
        """
        if bits == 32:
            return self._converter_para_ieee754_precisao_simples(numero)
        elif bits == 64:
            return self._converter_para_ieee754_precisao_dupla(numero)
        else:
            raise ValueError("Número de bits inválido para a representação IEEE 754.")

    def _converter_para_ieee754_precisao_simples(self, numero):
        """
        Converte um número para a representação de ponto flutuante de precisão simples IEEE 754.
        Parâmetros:
        - numero: O número a ser convertido.
        Retorna:
        - Um objeto bytes representando a representação IEEE 754 de precisão simples do número.
        """
        return struct.pack('>f', numero)

    def _converter_para_ieee754_precisao_dupla(self, numero):
        """
        Converte um número para a representação de ponto flutuante de precisão dupla IEEE 754.

        Parâmetros:
        - numero: O número a ser convertido.
        Retorna:
        - Um objeto bytes representando a representação IEEE 754 de precisão dupla do número.
        """
        return struct.pack('>d', numero)

    def _reverter_ieee_754(self, rxBuffer):
        """
        Reverte uma representação binária IEEE 754 para um número real.

        Parâmetros:
        - rxBuffer: O buffer de bytes que contém a representação binária IEEE 754 a ser revertida.
        Retorna:
        - O número real correspondente à representação binária.
        """
        # Determinar o comprimento do buffer para escolher a precisão correta
        if len(rxBuffer) == 4:
            return struct.unpack('>f', rxBuffer)[0]
        elif len(rxBuffer) == 8:
            return struct.unpack('>d', rxBuffer)[0]
        else:
            raise ValueError("Buffer length does not match IEEE 754 single or double precision.")
