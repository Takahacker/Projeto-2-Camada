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
        - Uma string representando a representação binária IEEE 754 do número.
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
        - Uma string representando a representação binária de precisão simples IEEE 754 do número.
        """
        # Converter para binário
        binario = bin(numero)[2:]
        # Dividir em sinal, expoente e mantissa
        sinal = '0' if numero >= 0 else '1'
        expoente = self._calcular_expoente_precisao_simples(numero)
        mantissa = self._calcular_mantissa_precisao_simples(numero)
        # Combinar e retornar
        return sinal + expoente + mantissa

    def _converter_para_ieee754_precisao_dupla(self, numero):
        """
        Converte um número para a representação de ponto flutuante de precisão dupla IEEE 754.
        
        Parâmetros:
        - numero: O número a ser convertido.
        
        Retorna:
        - Uma string representando a representação binária de precisão dupla IEEE 754 do número.
        """
        # Converter para binário
        binario = bin(numero)[2:]
        # Dividir em sinal, expoente e mantissa
        sinal = '0' if numero >= 0 else '1'
        expoente = self._calcular_expoente_precisao_dupla(numero)
        mantissa = self._calcular_mantissa_precisao_dupla(numero)
        # Combinar e retornar
        return sinal + expoente + mantissa

    def _calcular_expoente_precisao_simples(self, numero):
        """
        Calcula o expoente para a representação de ponto flutuante de precisão simples IEEE 754.
        Parâmetros:
        - numero: O número para calcular o expoente.
        Retorna:
        - Uma string representando o expoente em binário.
        """
        # Calcular o expoente
        expoente = int(numero).bit_length() + 127
        # Converter para binário e preencher com 8 bits
        return bin(expoente)[2:].zfill(8)

    def _calcular_mantissa_precisao_simples(self, numero):
        """
        Calcula a mantissa para a representação de ponto flutuante de precisão simples IEEE 754.
        Parâmetros:
        - numero: O número para calcular a mantissa.
        Retorna:
        - Uma string representando a mantissa em binário.
        """
        # Calcular a mantissa
        mantissa = numero - int(numero)
        binario_mantissa = ''
        for _ in range(23):  # 23 bits para precisão simples
            mantissa *= 2
            bit = int(mantissa)
            if bit == 1:
                binario_mantissa += '1'
                mantissa -= bit
            else:
                binario_mantissa += '0'
        return binario_mantissa

    def _calcular_expoente_precisao_dupla(self, numero):
        """
        Calcula o expoente para a representação de ponto flutuante de precisão dupla IEEE 754.
        Parâmetros:
        - numero: O número para calcular o expoente.
        Retorna:
        - Uma string representando o expoente em binário.
        """
        # Calcular o expoente
        expoente = int(numero).bit_length() + 1023
        # Converter para binário e preencher com 11 bits
        return bin(expoente)[2:].zfill(11)

    def _calcular_mantissa_precisao_dupla(self, numero):
        """
        Calcula a mantissa para a representação de ponto flutuante de precisão dupla IEEE 754.
        Parâmetros:
        - numero: O número para calcular a mantissa.
        Retorna:
        - Uma string representando a mantissa em binário.
        """
        # Calcular a mantissa
        mantissa = numero - int(numero)
        binario_mantissa = ''
        for _ in range(52):  # 52 bits para precisão dupla
            mantissa *= 2
            bit = int(mantissa)
            if bit == 1:
                binario_mantissa += '1'
                mantissa -= bit
            else:
                binario_mantissa += '0'
        return binario_mantissa

    def _reverter_ieee_754(self, rxBuffer):
        """
        Reverte uma representação binária IEEE 754 para um número real.
        
        Parâmetros:
        - rxBuffer: O buffer de bytes que contém a representação binária IEEE 754 a ser revertida.
        Retorna:
        - O número real correspondente à representação binária.
        """
        # Converte o buffer de bytes para uma string binária
        binario = ''.join(format(byte, '08b') for byte in rxBuffer)

        # Separa o binário em sinal, expoente e mantissa
        sinal = binario[0]
        expoente = binario[1:9]  # 8 bits para o expoente em precisão simples
        mantissa = binario[9:]    # 23 bits para a mantissa

        # Calcula o expoente real
        expoente_real = int(expoente, 2) - 127  # Para precisão simples, o bias é 127

        # Calcula a mantissa real
        mantissa_real = 1 + sum([2**-i for i, bit in enumerate(mantissa) if bit == '1'])

        # Calcula o número real
        numero_real = (-1)**int(sinal) * 2**expoente_real * mantissa_real

        return numero_real