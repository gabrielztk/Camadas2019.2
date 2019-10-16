#!/usr/bin/env python3

#importe as bibliotecas
from suaBibSignal import signalMeu
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import sys



def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    print("Inicializando encoder")
    #declare um objeto da classe da sua biblioteca de apoio (cedida)
    signal = signalMeu()
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    fs = 44100
    #tempo em segundos que ira emitir o sinal acustico 
    duration = 5
      
    #relativo ao volume. Um ganho alto pode saturar sua placa... comece com .3  
    gainX  = 0.3
    gainY  = 0.3


    print("Gerando Tons base")
    #Lista com relação de frequências
    FREQS = {
        "1": (697, 1209),
        "2": (697, 1336),
        "3": (697, 1477),
        "A": (697, 1633),
        "4": (770, 1209),
        "5": (770, 1336),
        "6": (770, 1477),
        "B": (770, 1633),
        "7": (852, 1209),
        "8": (852, 1336),
        "9": (852, 1477),
        "C": (852, 1633),
        "X": (941, 1209),
        "0": (941, 1336),
        "#": (941, 1477),
        "D": (941, 1633)
    }
    #Input para seleção de frequências, apenas valores de 0 a 9
    # Recusar outros valores
    while(True):
        NUM = input("Selecione um valor de 0 a 9 ou A, B, C, D, X e #: ")
        if NUM in FREQS:
            break
        else:
            print("Apenas valores mostrados podem ser selecionados")
    
    print("Gerando Tom referente ao símbolo : {}".format(NUM))
    #gere duas senoides para cada frequencia da tabela DTMF ! Canal x e canal y
    #use para isso sua biblioteca (cedida)
    canalX = signal.generateSin(FREQS[NUM][0], 1*gainX, duration, fs)
    canalY = signal.generateSin(FREQS[NUM][1], 1*gainY, duration, fs)
    #obtenha o vetor tempo
    tempo = canalX[0]
    #construa o sinal a ser reproduzido. Nâo se esqueca de que é a soma das senoides
    sinal = canalX[1] + canalY[1]
    #printe o grafico no tempo do sinal a ser reproduzido
    plt.plot(tempo[0:1000], sinal[0:1000])
    # reproduz o som
    sd.play(sinal, fs)
    # Exibe gráficos
    plt.show()
    # aguarda fim do audio
    sd.wait()

if __name__ == "__main__":
    main()
