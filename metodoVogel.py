from random import randint, shuffle
import time

def calculate_Penalidades(costos,costos_inversa):
    fila_penalidades = []
    columna_penalidades = []
    for i in costos:
        try:
            min1 = min(i)
            i.remove(min1)
            min2 = min(i)
        except:
            min1 = 0
            min2 = min1
        fila_penalidades.append(min2 - min1)
    for i in costos_inversa:
        try:
            min1 = min(i)
            i.remove(min1)
            min2 = min(i)
        except:
            min1 = 0
            min2 = min1
        columna_penalidades.append(min2 - min1)
    return fila_penalidades,columna_penalidades

def maxPenalidad(fila_penalidades,columna_penalidades):
    max_penalidad = max(fila_penalidades)
    isFila = True
    penalidad_index = fila_penalidades.index(max_penalidad)
    if max_penalidad < max(columna_penalidades):
        max_penalidad = max(columna_penalidades)
        isFila = False
        penalidad_index = columna_penalidades.index(max_penalidad)
    #Verificar Empate
    return isFila, penalidad_index

def costoMinimo(costo, costo_inversa, penalidad_index, isFila):
    if isFila:
        costo_min = min(costo[penalidad_index])
        costo_min_index = costo[penalidad_index].index(costo_min)
    else:
        costo_min = min(costo_inversa[penalidad_index])
        costo_min_index = costo_inversa[penalidad_index].index(costo_min)
    return costo_min_index

def asignarValor(solucion, penalidad_index, costo_min_index, isFila, copia_costos, copia_costo_inversa, plantas_capacidades, centros_demandas, fila_actuales, columna_actuales):
    if isFila:
        demanda = centros_demandas[fila_actuales[penalidad_index]]
        capacidad = plantas_capacidades[columna_actuales[costo_min_index]]
        if capacidad >= demanda:
            solucion[fila_actuales[penalidad_index]][columna_actuales[costo_min_index]] = demanda
            plantas_capacidades[columna_actuales[costo_min_index]] -= demanda
            centros_demandas[fila_actuales[penalidad_index]] -= demanda
        else:
            solucion[fila_actuales[penalidad_index]][columna_actuales[costo_min_index]] = capacidad
            plantas_capacidades[columna_actuales[costo_min_index]] -= capacidad
            centros_demandas[fila_actuales[penalidad_index]] -= capacidad
        fila_index = -1
        columna_index = -1
        if plantas_capacidades[columna_actuales[costo_min_index]] == 0:
            columna_index = costo_min_index
        if centros_demandas[fila_actuales[penalidad_index]] == 0:
            fila_index = penalidad_index
    else:
        demanda = plantas_capacidades[fila_actuales[costo_min_index]]
        capacidad = centros_demandas[columna_actuales[penalidad_index]]
        if capacidad >= demanda:
            solucion[fila_actuales[costo_min_index]][columna_actuales[penalidad_index]] = demanda
            plantas_capacidades[fila_actuales[costo_min_index]] -= demanda
            centros_demandas[columna_actuales[penalidad_index]] -= demanda
        else:
            solucion[fila_actuales[costo_min_index]][columna_actuales[penalidad_index]] = capacidad
            plantas_capacidades[fila_actuales[costo_min_index]] -= capacidad
            centros_demandas[columna_actuales[penalidad_index]] -= capacidad
        fila_index = -1
        columna_index = -1
        if centros_demandas[columna_actuales[penalidad_index]] == 0:
            fila_index = costo_min_index
        if plantas_capacidades[fila_actuales[costo_min_index]] == 0:
            columna_index = penalidad_index
    return solucion, plantas_capacidades, centros_demandas, fila_index, columna_index

def removerFilaColumna(copia_costos, copia_costos_inversa, fila_index, columna_index, fila_actuales, columna_actuales):
    if fila_index != -1:
        copia_costos.pop(fila_index)
        del copia_costos_inversa[:][fila_index]
        fila_actuales.pop(fila_index)
    if columna_index != -1:
        copia_costos_inversa.pop(columna_index)
        del copia_costos[:][columna_index]
        columna_actuales.pop(columna_index)
    return copia_costos, copia_costos_inversa, fila_actuales, columna_actuales

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

plantas_capacidades_original = plantas_capacidades.copy()
centros_demandas_original = centros_demandas.copy()

if(oferta_total > demanda_total):
    centros_demandas[randint(0,centros-1)] += oferta_total - demanda_total
elif (oferta_total < demanda_total):
    plantas_capacidades[randint(0,plantas-1)] += demanda_total - oferta_total

solucion = [[0 for x in range(plantas)] for i in range(centros)]

fila_actuales = [x for x in range(centros)]
columna_actuales = [x for x in range(plantas)]

copia_costos = costos_transporte.copy()
costos_inversa = []
for fila in range(plantas):
    fila_agregar = []
    for colum in range(centros):
        fila_agregar.append(costos_transporte[colum][fila])
    costos_inversa.append(fila_agregar)
copia_costos_inversa = costos_inversa.copy()

while True:
    fila_penalidades, columna_penalidades = calculate_Penalidades(copia_costos.copy(),copia_costos_inversa.copy())
    isFila, penalidad_index = maxPenalidad(fila_penalidades.copy(),columna_penalidades.copy())
    costo_min_index = costoMinimo(copia_costos.copy(), copia_costos_inversa.copy(), penalidad_index, isFila)
    solucion, plantas_capacidades, centros_demandas, fila_index, columna_index = asignarValor(solucion.copy(), penalidad_index, costo_min_index, isFila, copia_costos.copy(), copia_costos_inversa.copy(), plantas_capacidades.copy(), centros_demandas.copy(), fila_actuales.copy(), columna_actuales.copy())
    copia_costo, copia_costos_inversa, fila_actuales, columna_actuales = removerFilaColumna(copia_costos.copy(), copia_costos_inversa.copy(), fila_index, columna_index, fila_actuales.copy(), columna_actuales.copy())
    if len(fila_actuales) < 2 or len(columna_actuales) < 2:
        break

fo = 0
for i in range(centros):
    for j in range(plantas):
        fo += solucion[i][j] * costos_transporte[i][j]

print(numpy.array(solucion))
print(fo)