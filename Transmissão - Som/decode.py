#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
from suaBibSignal import signalMeu
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import pickle
#import peakutils


#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    print("Inicializando decoder")
    #declare um objeto da classe da sua biblioteca de apoio (cedida)
    signal = signalMeu()
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    fs = 44100
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    #taxa de amostragem
    #sd.default.samplerate = 1
    #voce pode ter que alterar isso dependendo da sua placa
    #sd.default.channels = 2  
    #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    duration = 1 
    # faca um printo na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    wait = 2
    print("A captura de som começará em {} segundos".format(wait))
    time.sleep(wait)
    #faca um print informando que a gravacao foi inicializada
    print("Gravação inicializada!")
    #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
    duracao = 3
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
    numAmostras = duracao*fs
    audio = sd.rec(int(numAmostras), samplerate=fs, channels=1)
    sd.wait()
    print("...     FIM")
    #grave uma variavel com apenas a parte que interessa (dados)


    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    tempo = np.linspace(0,duracao,numAmostras)
    # plot do gravico  áudio vs tempo!
    plt.plot(tempo[0:1000], audio[0:1000])


    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(audio, fs)
    plt.figure("F(y)")
    plt.plot(xf[0:1000],yf[0:1000])
    plt.grid()
    plt.title('Fourier audio')


    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.

    #index = peakutils.indexes(,,)

    #printe os picos encontrados! 

    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.


    ## Exibe gráficos
    plt.show()

if __name__ == "__main__":
    main()
