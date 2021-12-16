from random import randint, shuffle, randrange
from typing import Tuple
import numpy as np
import time
import copy

def obtener_fila_min_costo(max_pen_i, n_pen_i, pen_i, cij_aux, cij_sup, I, J):
    pen_filas = [x for x in range(I) if pen_i[x] == max_pen_i]
    min_costo = cij_sup + 1
    i_selec = 0
    for i in pen_filas:
        for j in range(J):
            if cij_aux[i][j] < min_costo and type(cij_aux[i][j]) is int:
                min_costo = cij_aux[i][j]
                i_selec = i
    return i_selec

def obtener_columna_min_costo(max_pen_j, n_pen_j, pen_j, cij_aux, cij_sup, J, I):
    pen_columnas = [x for x in range(J) if pen_j[x] == max_pen_j]
    min_costo = cij_sup + 1
    j_selec = 0
    for j in pen_columnas:
        for i in range(I):
            if cij_aux[i][j] < min_costo and type(cij_aux[i][j]) is int:
                min_costo = cij_aux[i][j]
                j_selec = j
    return j_selec

#Lectura de Parametros
plantas = int(input("Ingresar la cantidad de plantas de produccion: "))
centros = int(input("Ingresar la cantidad de centros de distribucion: "))
plantas_capacidad_inf = int(input("Ingrese el limite inferior de la capacidad de las plantas: "))
plantas_capacidad_sup = int(input("Ingrese el limite superior de la capacidad de las plantas: "))
centros_demanda_inf = int(input("Ingrese el limite inferior de la demanda de los centros: "))
centros_demanda_sup = int(input("Ingrese el limite superior de la demanda de los centros: "))
costo_transporte_inf = int(input("Ingrese el limite inferior para el costo de transporte: "))
costo_transporte_sup = int(input("Ingrese el limite superior para el costo de transporte: "))

plantas_capacidades = []
oferta_total = 0
for x in range(plantas):
    capacidad = randint(plantas_capacidad_inf,plantas_capacidad_sup)
    oferta_total += capacidad 
    #print("Planta de produccion "+str(x+1)+" tiene una capacidad de "+str(capacidad)+" productos")
    plantas_capacidades.append(capacidad)

centros_demandas = []
demanda_total = 0
for x in range(centros):
    demanda = randint(centros_demanda_inf,centros_demanda_sup)
    demanda_total += demanda
    #print("Centro de distribucion "+str(x+1)+" tiene una demanda de "+str(demanda)+" productos")
    centros_demandas.append(demanda)

costos_transporte = []
for x in range(centros):
    costos_planta_i= []
    for y in range(plantas):
        costo = randint(costo_transporte_inf,costo_transporte_sup)
        costos_planta_i.append(costo)
    #print("Costo de transporte de Planta "+str(x+1)+" :",costos_planta_i)
    costos_transporte.append(costos_planta_i)


if(oferta_total > demanda_total):
    centros_demandas[randint(0,centros-1)] += oferta_total - demanda_total
elif (oferta_total < demanda_total):
    plantas_capacidades[randint(0,plantas-1)] += demanda_total - oferta_total

plantas_capacidades_copy = copy.deepcopy(plantas_capacidades)
centros_demandas_copy = copy.deepcopy(centros_demandas)
costos_transporte_copy = copy.deepcopy(costos_transporte)

solucion = [[0 for x in range(plantas)] for i in range(centros)]

i = 0
j = 0
iteraciones = 0

plantas_capacidades_original = plantas_capacidades.copy()
centros_demandas_original = centros_demandas.copy()
time_start = time.time()
while True:
    iteraciones += 1
    solucion[i][j] = min(plantas_capacidades[j],centros_demandas[i])
    plantas_capacidades[j] -= solucion[i][j]
    centros_demandas[i] -= solucion[i][j]
    if(plantas_capacidades[j] < centros_demandas[i]):
        j += 1
    elif(plantas_capacidades[j] > centros_demandas[i]):
        i += 1
    else:
        i += 1
        j += 1
    if(plantas_capacidades[plantas-1] == 0 and centros_demandas[centros-1] == 0):
        break
time_end = time.time()

file = open("balanced_outputs_esquina/balanced_output_"+str(plantas)+"_"+str(centros)+".txt","w")

fo = 0
for i in range(centros):
    for j in range(plantas):
        fo += solucion[i][j] * costos_transporte[i][j]
    

file.write("Valor funcion objetivo = "+str(fo))
file.write("\n")
file.write("Cantidad de Iteraciones = "+str(iteraciones))
file.write("\n")
file.write("Tiempo de ejecucion (segundos) = "+str(time_end-time_start))
file.write("\n\n")


max_length = 0
for x in plantas_capacidades_original:
    max_length = max(max_length,len(str(x)))

j = 0
for x in solucion:
    for i in x:
        file.write(str(i)+" "*(max_length+1-len(str(i))))
    file.write("| "+str(centros_demandas_original[j]))
    j += 1
    file.write("\n")

file.write("-"*((max_length+1)*plantas+1))
file.write("\n")
for x in plantas_capacidades_original:
    file.write(str(x)+" "*(max_length+1-len(str(x))))
file.write("\n")
file.close()


plantas_capacidades = plantas_capacidades_original.copy()
centros_demandas = centros_demandas_original.copy()
shuffle(plantas_capacidades)
shuffle(centros_demandas)
plantas_capacidades_copy_2 = copy.deepcopy(plantas_capacidades)
centros_demandas_copy_2 = copy.deepcopy(centros_demandas)
plantas_capacidades_original_2 = plantas_capacidades.copy()
centros_demandas_original_2 = centros_demandas.copy()
i = 0
j = 0
iteraciones = 0
solucion = [[0 for x in range(plantas)] for i in range(centros)]
time_start = time.time()
while True:
    iteraciones += 1
    solucion[i][j] = min(plantas_capacidades[j],centros_demandas[i])
    plantas_capacidades[j] -= solucion[i][j]
    centros_demandas[i] -= solucion[i][j]
    if(plantas_capacidades[j] < centros_demandas[i]):
        j += 1
    elif(plantas_capacidades[j] > centros_demandas[i]):
        i += 1
    else:
        i += 1
        j += 1
    if(plantas_capacidades[plantas-1] == 0 and centros_demandas[centros-1] == 0):
        break
time_end = time.time()

file = open("balanced_outputs_esquina/balanced_output_"+str(plantas)+"_"+str(centros)+"_costosfijos.txt","w")

fo = 0
for i in range(centros):
    for j in range(plantas):
        fo += solucion[i][j] * costos_transporte[i][j]
    

file.write("Valor funcion objetivo = "+str(fo))
file.write("\n")
file.write("Cantidad de Iteraciones = "+str(iteraciones))
file.write("\n")
file.write("Tiempo de ejecucion (segundos) = "+str(time_end-time_start))
file.write("\n\n")


j = 0
for x in solucion:
    for i in x:
        file.write(str(i)+" "*(max_length+1-len(str(i))))
    file.write("| "+str(centros_demandas_original_2[j]))
    j += 1
    file.write("\n")

file.write("-"*((max_length+1)*plantas+1))
file.write("\n")
for x in plantas_capacidades_original_2:
    file.write(str(x)+" "*(max_length+1-len(str(x))))
file.write("\n")
file.close()

plantas_capacidades = plantas_capacidades_original.copy()
centros_demandas = centros_demandas_original.copy()
i = 0
j = 0
iteraciones = 0
solucion = [[0 for x in range(plantas)] for i in range(centros)]
time_start = time.time()
while True:
    iteraciones += 1
    solucion[i][j] = min(plantas_capacidades[j],centros_demandas[i])
    plantas_capacidades[j] -= solucion[i][j]
    centros_demandas[i] -= solucion[i][j]
    if(plantas_capacidades[j] < centros_demandas[i]):
        j += 1
    elif(plantas_capacidades[j] > centros_demandas[i]):
        i += 1
    else:
        i += 1
        j += 1
    if(plantas_capacidades[plantas-1] == 0 and centros_demandas[centros-1] == 0):
        break
time_end = time.time()

file = open("balanced_outputs_esquina/balanced_output_"+str(plantas)+"_"+str(centros)+"_centrosplantasfijas.txt","w")

shuffle(costos_transporte)
costos_transporte_copy_2 = copy.deepcopy(costos_transporte)
fo = 0
for i in range(centros):
    for j in range(plantas):
        fo += solucion[i][j] * costos_transporte[i][j]
    

file.write("Valor funcion objetivo = "+str(fo))
file.write("\n")
file.write("Cantidad de Iteraciones = "+str(iteraciones))
file.write("\n")
file.write("Tiempo de ejecucion (segundos) = "+str(time_end-time_start))
file.write("\n\n")

j = 0
for x in solucion:
    for i in x:
        file.write(str(i)+" "*(max_length+1-len(str(i))))
    file.write("| "+str(centros_demandas_original[j]))
    j += 1
    file.write("\n")

file.write("-"*((max_length+1)*plantas+1))
file.write("\n")
for x in plantas_capacidades_original:
    file.write(str(x)+" "*(max_length+1-len(str(x))))
file.write("\n")
file.close()

I = centros
J = plantas
cij_sup = costo_transporte_sup + 1
dj = copy.deepcopy(plantas_capacidades_copy)
oi = copy.deepcopy(centros_demandas_copy)
cij = copy.deepcopy(costos_transporte_copy)
oi_aux = copy.deepcopy(oi)
dj_aux = copy.deepcopy(dj)
cij_aux = copy.deepcopy(cij)

xij = [[0 for x in range(plantas)] for x in range(centros)]

pen_i = list(np.ones(I))
pen_j = list(np.ones(J))
flag_i = True
flag_j = True
iteraciones = 0
time_start = time.time()
while True:
    iteraciones += 1
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
            if cij_aux[i_selec][j] < min_costo and cij_aux[i_selec][j] != True:
                min_costo = cij_aux[i_selec][j]
        j_selec = cij_aux[i_selec].index(min_costo)
    elif max_pen_i < max_pen_j:
        if n_pen_j == 1:
            j_selec = pen_j.index(max_pen_j)
        else:
            j_selec = obtener_columna_min_costo(max_pen_j, n_pen_j, pen_j, cij_aux, cij_sup, J, I)
        for i in range(I):
            if cij_aux[i][j_selec] < min_costo and cij_aux[i][j_selec] != True:
                min_costo = cij_aux[i][j_selec]
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
            if cij_aux[i_candidato][j] < min_costo_fila and cij_aux[i_candidato][j] != True:
                min_costo_fila = cij_aux[i_candidato][j]
        j_posible = cij_aux[i_candidato].index(min_costo_fila)
        for i in range(I):
            if cij_aux[i][j_candidato] < min_costo_col and cij_aux[i][j_candidato] != True:
                min_costo_col = cij_aux[i][j_candidato]
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
time_end = time.time()

file = open("balanced_outputs_vogel/balanced_output_"+str(plantas)+"_"+str(centros)+".txt","w")

fo = 0
for i in range(centros):
    for j in range(plantas):
        fo += xij[i][j]*cij[i][j]
    
    
file.write("Valor funcion objetivo = "+str(fo))
file.write("\n")
file.write("Cantidad de Iteraciones = "+str(iteraciones))
file.write("\n")
file.write("Tiempo de ejecucion (segundos) = "+str(time_end-time_start))
file.write("\n\n")


max_length = 0
for x in plantas_capacidades_original:
    max_length = max(max_length,len(str(x)))

j = 0
for x in xij:
    for i in x:
        file.write(str(i)+" "*(max_length+1-len(str(i))))
    file.write("| "+str(centros_demandas_original[j]))
    j += 1
    file.write("\n")

file.write("-"*((max_length+1)*plantas+1))
file.write("\n")
for x in plantas_capacidades_original:
    file.write(str(x)+" "*(max_length+1-len(str(x))))
file.write("\n")
file.close()

I = centros
J = plantas
cij_sup = costo_transporte_sup + 1
dj = copy.deepcopy(plantas_capacidades_copy_2)
oi = copy.deepcopy(centros_demandas_copy_2)
cij = copy.deepcopy(costos_transporte_copy)
plantas_capacidades_original_2 = copy.deepcopy(dj)
centros_demandas_original_2 = copy.deepcopy(oi)
oi_aux = copy.deepcopy(oi)
dj_aux = copy.deepcopy(dj)
cij_aux = copy.deepcopy(cij)

xij = [[0 for x in range(plantas)] for x in range(centros)]

pen_i = list(np.ones(I))
pen_j = list(np.ones(J))
flag_i = True
flag_j = True
iteraciones = 0
time_start = time.time()
while True:
    iteraciones += 1
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
            if cij_aux[i_selec][j] < min_costo and cij_aux[i_selec][j] != True:
                min_costo = cij_aux[i_selec][j]
        j_selec = cij_aux[i_selec].index(min_costo)
    elif max_pen_i < max_pen_j:
        if n_pen_j == 1:
            j_selec = pen_j.index(max_pen_j)
        else:
            j_selec = obtener_columna_min_costo(max_pen_j, n_pen_j, pen_j, cij_aux, cij_sup, J, I)
        for i in range(I):
            if cij_aux[i][j_selec] < min_costo and cij_aux[i][j_selec] != True:
                min_costo = cij_aux[i][j_selec]
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
            if cij_aux[i_candidato][j] < min_costo_fila and cij_aux[i_candidato][j] != True:
                min_costo_fila = cij_aux[i_candidato][j]
        j_posible = cij_aux[i_candidato].index(min_costo_fila)
        for i in range(I):
            if cij_aux[i][j_candidato] < min_costo_col and cij_aux[i][j_candidato] != True:
                min_costo_col = cij_aux[i][j_candidato]
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
time_end = time.time()

file = open("balanced_outputs_vogel/balanced_output_"+str(plantas)+"_"+str(centros)+"_costosfijos.txt","w")

fo = 0
for i in range(centros):
    for j in range(plantas):
        fo += xij[i][j]*cij[i][j]
    
file.write("Valor funcion objetivo = "+str(fo))
file.write("\n")
file.write("Cantidad de Iteraciones = "+str(iteraciones))
file.write("\n")
file.write("Tiempo de ejecucion (segundos) = "+str(time_end-time_start))
file.write("\n\n")


max_length = 0
for x in plantas_capacidades_original_2:
    max_length = max(max_length,len(str(x)))

j = 0
for x in xij:
    for i in x:
        file.write(str(i)+" "*(max_length+1-len(str(i))))
    file.write("| "+str(centros_demandas_original_2[j]))
    j += 1
    file.write("\n")

file.write("-"*((max_length+1)*plantas+1))
file.write("\n")
for x in plantas_capacidades_original_2:
    file.write(str(x)+" "*(max_length+1-len(str(x))))
file.write("\n")
file.close()

I = centros
J = plantas
cij_sup = costo_transporte_sup + 1
dj = copy.deepcopy(plantas_capacidades_copy)
oi = copy.deepcopy(centros_demandas_copy)
cij = copy.deepcopy(costos_transporte_copy_2)
oi_aux = copy.deepcopy(oi)
dj_aux = copy.deepcopy(dj)
cij_aux = copy.deepcopy(cij)


xij = [[0 for x in range(plantas)] for x in range(centros)]


pen_i = list(np.ones(I))
pen_j = list(np.ones(J))
flag_i = True
flag_j = True
iteraciones = 0
time_start = time.time()
while True:
    iteraciones += 1
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
            if cij_aux[i_selec][j] < min_costo and cij_aux[i_selec][j] != True:
                min_costo = cij_aux[i_selec][j]
        j_selec = cij_aux[i_selec].index(min_costo)
    elif max_pen_i < max_pen_j:
        if n_pen_j == 1:
            j_selec = pen_j.index(max_pen_j)
        else:
            j_selec = obtener_columna_min_costo(max_pen_j, n_pen_j, pen_j, cij_aux, cij_sup, J, I)
        for i in range(I):
            if cij_aux[i][j_selec] < min_costo and cij_aux[i][j_selec] != True:
                min_costo = cij_aux[i][j_selec]
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
            if cij_aux[i_candidato][j] < min_costo_fila and cij_aux[i_candidato][j] != True:
                min_costo_fila = cij_aux[i_candidato][j]
        j_posible = cij_aux[i_candidato].index(min_costo_fila)
        for i in range(I):
            if cij_aux[i][j_candidato] < min_costo_col and cij_aux[i][j_candidato] != True:
                min_costo_col = cij_aux[i][j_candidato]
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
time_end = time.time()

file = open("balanced_outputs_vogel/balanced_output_"+str(plantas)+"_"+str(centros)+"_centrosplantasfijas.txt","w")

fo = 0
for i in range(centros):
    for j in range(plantas):
        fo += xij[i][j]*cij[i][j]
    
file.write("Valor funcion objetivo = "+str(fo))
file.write("\n")
file.write("Cantidad de Iteraciones = "+str(iteraciones))
file.write("\n")
file.write("Tiempo de ejecucion (segundos) = "+str(time_end-time_start))
file.write("\n\n")


max_length = 0
for x in plantas_capacidades_original:
    max_length = max(max_length,len(str(x)))

j = 0
for x in xij:
    for i in x:
        file.write(str(i)+" "*(max_length+1-len(str(i))))
    file.write("| "+str(centros_demandas_original[j]))
    j += 1
    file.write("\n")

file.write("-"*((max_length+1)*plantas+1))
file.write("\n")
for x in plantas_capacidades_original:
    file.write(str(x)+" "*(max_length+1-len(str(x))))
file.write("\n")
file.close()