from random import randint, shuffle
import time

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