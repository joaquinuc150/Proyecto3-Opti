from random import randint, randrange
from typing import Tuple
import numpy as np

#Lectura de Parametros
plantas = int(input("Ingresar la cantidad de plantas de produccion: "))
centros = int(input("Ingresar la cantidad de centros de distribucion: "))
plantas_capacidad_inf = int(input("Ingrese el limite inferior de la capacidad de las plantas: "))
plantas_capacidad_sup = int(input("Ingrese el limite superior de la capacidad de las plantas: "))
centros_demanda_inf = int(input("Ingrese el limite inferior de la demanda de los centros: "))
centros_demanda_sup = int(input("Ingrese el limite superior de la demanda de los centros: "))
costo_transporte_inf = int(input("Ingrese el limite inferior para el costo de transporte: "))
costo_transporte_sup = int(input("Ingrese el limite superior para el costo de transporte: "))

I = centros
J = plantas
cij_sup = costo_transporte_sup + 1
dj = []
oferta_total = 0
for x in range(plantas):
    capacidad = randint(plantas_capacidad_inf,plantas_capacidad_sup)
    oferta_total += capacidad 
    #print("Planta de produccion "+str(x+1)+" tiene una capacidad de "+str(capacidad)+" productos")
    dj.append(capacidad)

oi = []
demanda_total = 0
for x in range(centros):
    demanda = randint(centros_demanda_inf,centros_demanda_sup)
    demanda_total += demanda
    #print("Centro de distribucion "+str(x+1)+" tiene una demanda de "+str(demanda)+" productos")
    oi.append(demanda)

cij = []
for x in range(centros):
    costos_planta_i= []
    for y in range(plantas):
        costo = randint(costo_transporte_inf,costo_transporte_sup)
        costos_planta_i.append(costo)
    #print("Costo de transporte de Planta "+str(x+1)+" :",costos_planta_i)
    cij.append(costos_planta_i)


if(oferta_total > demanda_total):
    oi[randint(0,centros-1)] += oferta_total - demanda_total
elif (oferta_total < demanda_total):
    dj[randint(0,plantas-1)] += demanda_total - oferta_total

oi_aux = oi.copy()
dj_aux = dj.copy()
cij_aux = cij.copy()

xij = [[0 for x in range(plantas)] for x in range(centros)]

def fo(xij, cij):
    suma = 0
    for i in range(I):
        for j in range(J):
            suma += xij[i][j]*cij[i][j]
    return suma

def obtener_fila_min_costo(max_pen_i, n_pen_i, pen_i, cij_aux, cij_sup, I, J):
    min_costo = cij_sup + 1
    i_selec = 0
    for i in range(I):
        if pen_i[i] == max_pen_i:
            for j in range(J):
                costo = cij_aux[i][j]
                if costo < min_costo and costo != True:
                    min_costo = costo
                    i_selec = i
    return i_selec

def obtener_columna_min_costo(max_pen_j, n_pen_j, pen_j, cij_aux, cij_sup, J, I):
    min_costo = cij_sup + 1
    j_selec = 0
    for j in range(J):
        if pen_j[j] == max_pen_j:
            for i in range(I):
                costo = cij_aux[i][j]
                if costo < min_costo and costo != True:
                    min_costo = costo
                    j_selec = j
    return j_selec

pen_i = list(np.ones(I))
pen_j = list(np.ones(J))
flag_i = True
flag_j = True
while True:
    arreglo = np.array(cij_aux)
    if flag_i == True:
        for i in range(I):
            j_menor = 0
            min_costo1 = cij_sup + 1
            min_costo2 = cij_sup + 1
            if pen_i[i] != -1:
                for j in range(J):
                    if cij_aux[i][j] < min_costo1 and cij_aux[i][j] != True:
                        min_costo1 = cij_aux[i][j]
                        j_menor = j
                for j in range(J):
                    if cij_aux[i][j] < min_costo1 and cij_aux[i][j] != True and j != j:
                        min_costo2 = cij_aux[i][j]
                pen_i[i] = min_costo2 - min_costo1
    if flag_j == True:
        for j in range(J):
            i_menor = 0
            min_costo1 = cij_sup + 1
            min_costo2 = cij_sup + 1
            if pen_j[j] != -1:
                for i in range(I):
                    if cij_aux[i][j] < min_costo1 and cij_aux[i][j] != True:
                        min_costo1 = cij_aux[i][j]
                        i_menor = i
                for i in range(I):
                    if cij_aux[i][j] < min_costo1 and cij_aux[i][j] != True and i != i:
                        min_costo2 = cij_aux[i][j]
                pen_j[j] = min_costo2 - min_costo1
    max_pen_i = np.array(pen_i).max()
    n_pen_i = pen_i.count(max_pen_i)
    max_pen_j = np.array(pen_j).max()
    n_pen_j = pen_j.count(max_pen_j)
    min_costo = cij_sup + 1
    min_costo_fila = cij_sup + 1
    min_costo_col = cij_sup + 1
    if max_pen_i > max_pen_j:
        if n_pen_i == 1:
            i_selec = pen_i.index(max_pen_i)
        else:
            i_selec = obtener_fila_min_costo(max_pen_i, n_pen_i, pen_i, cij_aux, cij_sup, I, J)
        for j in range(J):
            if cij_aux[i_selec][j] < min_costo and type(cij_aux[i_selec][j]) is int:
                min_costo = cij_aux[i_selec][j]
                print(min_costo)
        j_selec = cij_aux[i_selec].index(min_costo)
    elif max_pen_i < max_pen_j:
        if n_pen_j == 1:
            j_selec = pen_j.index(max_pen_j)
        else:
            j_selec = obtener_columna_min_costo(max_pen_j, n_pen_j, pen_j, cij_aux, cij_sup, J, I)
        for i in range(I):
            if cij_aux[i][j_selec] < min_costo and type(cij_aux[i][j_selec]) is int:
                min_costo = cij_aux[i][j_selec]
                print(min_costo)
        i_selec = list(np.array(cij_aux)[:,j_selec]).index(min_costo)
    elif max_pen_i == max_pen_j:
        if n_pen_i > 1:
            i_candidato = obtener_fila_min_costo(max_pen_i, n_pen_i, pen_i, cij_aux, cij_sup, I, J)
        else:
            i_candidato = pen_i.index(max_pen_i)
        if n_pen_j > 1:
            j_candidato = obtener_columna_min_costo(max_pen_j, n_pen_j, pen_j, cij_aux, cij_sup, J, I)
        else:
            j_candidato = pen_j.index(max_pen_j)
        for j in range(J):
            if cij_aux[i_candidato][j] < min_costo_fila and type(cij_aux[i_candidato][j]) is int:
                min_costo_fila = cij_aux[i_candidato][j]
                print(min_costo_fila)
        j_posible = cij_aux[i_candidato].index(min_costo_fila)
        for i in range(I):
            if cij_aux[i][j_candidato] < min_costo_col and type(cij_aux[i][j_candidato]) is int:
                min_costo_col = cij_aux[i][j_candidato]
                print(min_costo_col)
        i_posible = list(np.array(cij_aux)[:,j_candidato]).index(min_costo_col)
        if min_costo_fila < min_costo_col:
            i_selec = i_candidato
            j_selec = j_posible
        else:
            j_selec = j_candidato
            i_selec = i_posible
    xij[i_selec][j_selec] = min(oi_aux[i_selec], dj_aux[j_selec])
    oi_aux[i_selec] -= xij[i_selec][j_selec]
    dj_aux[j_selec] -= xij[i_selec][j_selec]
    if oi_aux[i_selec] < dj_aux[j_selec]:
        pen_i[i_selec] = -1
        for j in range(J):
            cij_aux[i_selec][j] = True
        flag_i = False
        flag_j = True
    elif oi_aux[i_selec] > dj_aux[j_selec]:
        pen_j[j_selec] = -1
        for i in range(I):
            cij_aux[i][j_selec] = True
        flag_i = True
        flag_j = False
    else:
        pen_i[i_selec] = -1
        pen_j[j_selec] = -1
        for j in range(J):
            cij_aux[i_selec][j] = True
        for i in range(I):
            cij_aux[i][j_selec] = True
        flag_i = True
        flag_j = True
    if np.array(oi_aux).sum() == 0 and np.array(dj_aux).sum() == 0:
        break
print()
print(np.array(xij))
valor_fo = fo(xij,cij)
print("Valor funcion objetivo = ", valor_fo)