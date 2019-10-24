#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
from suaBibSignal import signalMeu
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import pickle
import peakutils
import math


#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

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

    array = [
        [],
        [],
        [],
        []
    ]

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
    # faca um printo na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    wait = 5
    print("A captura de som começará em {} segundos".format(wait))
    time.sleep(wait)
    #faca um print informando que a gravacao foi inicializada
    print("Gravação inicializada!")
    #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
    duracao = 3
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
    numAmostras = duracao*fs
    audio = sd.rec(int(numAmostras), samplerate=fs, channels=2)
    sd.wait()
    print("...     FIM")
    #grave uma variavel com apenas a parte que interessa (dados)
    sinal = []
    for u in audio:
        sinal.append(u[0])
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    tempo = np.linspace(0,duracao,numAmostras)
    # plot do gravico  áudio vs tempo!
    plt.plot(tempo, sinal)
    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(sinal, fs)
    plt.figure("F(y)")
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')
    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
    indexes = peakutils.indexes(yf, thres=0.4, min_dist=100)
    #printe os picos encontrados!

    x_max = []

    for index in indexes:
        if xf[index] < 1800 and xf[index] > 500:
            math.isclose(2.547, 2.0048, abs_tol = 0.5)
            x_max.append(xf[index])
            print(xf[index])

    for e in FREQS:
        if math.isclose(FREQS[e][0], x_max[0], abs_tol = 0.5) and math.isclose(FREQS[e][1], x_max[1], abs_tol = 0.5):
            print("A tecla apertada foi: {}".format(e))
        else:
            pass

    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.


    ## Exibe gráficos
    plt.show()

if __name__ == "__main__":
    main()
