import matplotlib.pyplot as plt
import numpy as np
import random
import multiprocessing as mp
import os
import math 
import time
import imageio.v3 as img

def initGrids(size):
    a = np.zeros((size, size), dtype = int)
    return a

def initCellsAlive(Grid):
    currentGrid = Grid
    cellCount = len(Grid[0])
    amountOfStartingPts = int(len(Grid)*len(Grid)*0.2)
    for i in range(amountOfStartingPts):
        xAxis = random.randrange(0, cellCount)
        yAxis = random.randrange(0, cellCount)
        currentGrid[xAxis, yAxis] = 1
    return currentGrid

def checkNeighbours(Grid, concatGrids, vectors, i):
    ide = int(i)
    vector = int(vectors[ide])
    currentGrid = Grid.copy()
    updatedGrid = np.zeros((vector, len(Grid)), dtype=int)
    for row, col in np.ndindex((vector, len(Grid))):
        print(vector)
        numOfNbs = np.sum(currentGrid[(int(row) + (vector * int(ide)) - vector) - 1:(int(row) + (vector * int(ide)) - vector) + 2, col - 1:col + 2], initial=0) - currentGrid[(int(row) + (vector * int(ide)) - vector)][col]         
        if(numOfNbs < 0):
            numOfNbs = 0
        updatedGrid[row][col] = numOfNbs
    NbrMask = updatedGrid.copy()
    newGrid = np.zeros((vector, len(Grid)), dtype=int)

    for row, col in np.ndindex(vector, len(Grid)):
        if(currentGrid[(int(row) + (vector * int(ide)) - vector)][col] == 1):
            if(NbrMask[row][col] < 2 or NbrMask[row][col] > 3):
                newGrid[row][col] == 0
            elif(NbrMask[row][col] == 2 or NbrMask[row][col] == 3):
                newGrid[row][col] = 1            
        if(currentGrid[(int(row) + (vector * int(ide)) - vector)][col] == 0):
            if(NbrMask[row][col] == 3):
                newGrid[row][col] = 1
    concatGrids[int(ide)] = newGrid

def createVectors(Grid, cpuCount):
    wszystkie_liczby = range(0, len(Grid))
    vectors = []
    for i in range(cpuCount):
        vectors.append((i+1)*len(wszystkie_liczby)//cpuCount - (i*len(wszystkie_liczby)//cpuCount))
    print(vectors)    
    return vectors

def createFrame(concatGrids):
    cgArray = concatGrids[::-1]
    temp = np.concatenate(cgArray, axis=0)    
    concatGrids = []
    print(temp)
    return(temp)

def barPlot(chartCPUs, chartTimes, size):
    plt.bar(chartCPUs, chartTimes)
    plt.xlabel('ilosc watkow')
    plt.ylabel('czas trwania')
    filename = f'x{size}x{size}cpu{cpuCount}.png'
    plt.savefig(filename)
    plt.close()

def gifCreation(gifArray, cpuCount, size):
    filenames = []
    index = 0
    frames = 4
    for i in gifArray:
        img = i
        cmap = 'Greys_r'
        plt.matshow(img, cmap=cmap)
        filename = f'{cpuCount}{size}{index}planszawatkow.png'
        for i in range(frames):
            filenames.append(filename)
        index+=1 
        plt.savefig(filename)
        plt.close()
    import imageio.v2 as imageio
    with imageio.get_writer(f"gif.gif", mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)     
    import os
    # Remove files
    for filename in set(filenames):
        os.remove(filename)
    
if __name__ == "__main__":
    n = [16, 32]    # rozmiary plansz
    for j in range(len(n)):
        size = n[j]
        chartCPUs = []
        chartTimes = []    #zmienne używane w tworzeniu wykresów
        filenames = []
        for i in range(8):
            gifArray = []                      ##  zmienna przechowująca klatki do GIFa
            cpuCount = i + 1                    #  Ilość wątków
            Grid = initGrids(size)              #  konstruktor planszy
            menager = mp.Manager()              #  menager pamięci wieloprocesowej
            concatGrids = menager.list()        #  array do konkatenacji strumienia komórek w tablice 2d
            gifConstructor = menager.list()    ##  zmienna konstruktor GIF
            for ide in range(cpuCount):                                      
                concatGrids.append([ide])  # deklaracja ilości komóek odpowiadającej ilości procesów
            Grid = initCellsAlive(Grid)  #deklaracja żywych komórek początkowych
            print(Grid)
            vectors = createVectors(Grid, cpuCount) # tworzenie wektorów
            times = 1
            start = time.perf_counter() # czas startu aplikacji
            while(times <= 1):
                p = [mp.Process(target=checkNeighbours, args=(Grid, concatGrids, vectors, i)) for i in range(cpuCount)]    #lista procesów
                for i in p:
                    i.start()    #procesy startują
                for i in p:
                    i.join()    #procesy czekają na siebie przed rozpoczęciem kolejnego cyklu
                Grid = createFrame(concatGrids) #plansza po konkatenacji
                times+=1
                gifArray.append(Grid)          
            stop = time.perf_counter() #koniec czasu wykonania danej kolejki
            print(f"program wykonywał się  {stop - start} sekund dla {cpuCount} rdzeni")
            runTime =(stop - start) 
            chartCPUs.append(cpuCount)
            chartTimes.append(runTime)
            if(cpuCount < 3):
                gifCreation(gifArray, cpuCount, size) 
        barPlot(chartCPUs, chartTimes, size)
   
   
   
   

