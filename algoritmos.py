import math
from itertools import combinations

#ALGORITMO FUERZA BRUTA

def gananciaCombinacion(combinacion):
  ganancia = 0
  for i in range(0, len(combinacion)):
    ganancia += (combinacion[i][0] * combinacion[i][1])  #Precio * accion
  return ganancia  ## COMPLEJIDAD O(n)


def obtenerCombinaciones(A, n, ofertas):
  ganancia = 0
  todas_combinaciones = []
  for tamano_combinacion in range(1, n + 1):
    for combinacion in combinations(ofertas[:-1], tamano_combinacion):
      num_acciones = sum(x[1] for x in combinacion)
      oferta_faltante = (ofertas[-1][0], A - num_acciones)
      if oferta_faltante[1] >= 0:
        todas_combinaciones.append(list(combinacion) + [oferta_faltante])

  return todas_combinaciones


def accionesFB(entrada):
  archivo = open(entrada, "r")
  tuplas=[]

  A = int(archivo.readline().strip())
  B = int(archivo.readline().strip())
  n = int(archivo.readline().strip())

  for _ in range(0):
    archivo.readline()
  for _ in range(4, n+4):
    linea = archivo.readline().strip()
    elementos = linea.split()
    tupla = tuple(elementos)
    tuplas.append(tupla)

  ofertas = [tuple(map(int, elemento[0].split(','))) for elemento in tuplas]
  n = len(ofertas)-1 
  
  mejorCombinacion = 0
  ganancia = 0
  combinaciones = obtenerCombinaciones(A, n, ofertas)  # O(n*2^n)
  for i in range(0, len(combinaciones)):  # O(2^n)
    if gananciaCombinacion(combinaciones[i]) > ganancia:
      ganancia = gananciaCombinacion(combinaciones[i])
      mejorCombinacion = i
  acciones = []
  for oferta in ofertas[:-1]:
    if oferta in combinaciones[mejorCombinacion]:
      acciones.append([
        x[1] for x in combinaciones[mejorCombinacion]
        if x[0] == oferta[0] and x[1] == oferta[1] and x[2] == oferta[2]][0])
    else:
      acciones.append(0)
  acciones.append(A - sum(acciones))

  salida = str(ganancia) + " " + str(acciones)
  return salida


#ALGORITMO VORÁZ

def accionesV(entrada):
  archivo = open(entrada, "r")
  tuplas=[]

  A = int(archivo.readline().strip())
  B = int(archivo.readline().strip())
  n = int(archivo.readline().strip())

  for _ in range(0):
    archivo.readline()
  for _ in range(4, n+4):
    linea = archivo.readline().strip()
    elementos = linea.split()
    tupla = tuple(elementos)
    tuplas.append(tupla)

  ofertas = [tuple(map(int, elemento[0].split(','))) for elemento in tuplas]
  n = len(ofertas)-1 

  solucion = [0] * n
  tuplas = []  # [(plataRecibida, indice), (plataRecibida, indice)]

  for i in range(n):
    p = ofertas[i][0]  #precio por acción.
    c = ofertas[i][1]  #numero máximo de acciones
    ganancia = p * c
    tuplas.append([ganancia, i])

  tuplaOrdenada = sorted(tuplas, key=lambda tupla: tupla[0], reverse=True)
  for i in range(n):
    gananciaMax = tuplaOrdenada[0]
    indexGanMax = gananciaMax[1]

    p = ofertas[i][0]  #precio por acción.
    c = ofertas[indexGanMax][1]  #numero máximo de acciones
    r = ofertas[indexGanMax][2]  #numero minimo de acciones

    if B <= p:
      if A >= c:
        solucion[indexGanMax] = ofertas[indexGanMax][1]
        A = A - c

      elif r <= A:  ## Significa que A está entre c y r
        solucion[indexGanMax] = A
        A = 0
    del tuplaOrdenada[0]

  solucion.append(A)

  ganancia_total = 0
  for i in range(n+1):
    p = ofertas[i][0]
    c = solucion[i]
    ganancia_total += p * c

  salida = str(ganancia_total) + " " + str(solucion)
  return salida


#ALGORITMO DINÁMICA 1

def accionesPD1_costo(i, A, ofertas,tabla):
    inf = math.inf
    if i == len(ofertas):
        return 0
    if tabla[i][A] != inf:
        return tabla[i][A]
    p, c, r = ofertas[i]
    solucion = accionesPD1_costo(i+1, A, ofertas,tabla)
    for k in range(r, min(A, c)+1):
        solucion = max(solucion, p*k + accionesPD1_costo(i+1, A-k, ofertas,tabla))
    tabla[i][A] = solucion

    return solucion


def accionesPD1(entrada):
  archivo = open(entrada, "r")
  tuplas=[]

  A = int(archivo.readline().strip())
  B = int(archivo.readline().strip())
  n = int(archivo.readline().strip())

  for _ in range(0):
    archivo.readline()
  for _ in range(4, n+4):
    linea = archivo.readline().strip()
    elementos = linea.split()
    tupla = tuple(elementos)
    tuplas.append(tupla)

  ofertas = [tuple(map(int, elemento[0].split(','))) for elemento in tuplas]
  n = len(ofertas)-1 
  
  inf = math.inf
  tabla = [[inf for i in range(A+1)] for i in range(n+1)]
  solucion = [0]*(n+1)
  optimal = accionesPD1_costo(0, A, ofertas, tabla)
  for i in range(n):
    p,c,r = ofertas[i]
    for k in range(r, min(A, c)+1):
      if tabla[i][A] == p*k + tabla[i+1][A-k]:
        solucion[i] = k
        A=A-k
        break
  solucion[-1] = A
  salida = str(optimal) + " " + str(solucion)
  return salida



#ALGORITMO DINÁMICA 2

def accionesPD2_costo(i, A, ofertas, tabla, M):
  inf = math.inf
  j = int(A/M)           # Cantidad de columnas
  if i == len(ofertas):
    return 0
  if tabla[i][j] != inf:
    return tabla[i][j]
  p, c, r = ofertas[i]
  c = int(c/M)
  r = int(r/M)
  solucion = accionesPD2_costo(i + 1, A, ofertas, tabla,M)
  for k in range(r, min(j, c) + 1):
    solucion =max(solucion, p * (k * M) + accionesPD2_costo(i + 1, A - k*M, ofertas, tabla,M))
  tabla[i][j] = solucion
  return solucion
  
def accionesPD2(entrada):
  archivo = open(entrada, "r")
  tuplas=[]

  A = int(archivo.readline().strip())
  B = int(archivo.readline().strip())
  n = int(archivo.readline().strip())

  for _ in range(0):
    archivo.readline()
  for _ in range(4, n+4):
    linea = archivo.readline().strip()
    elementos = linea.split()
    tupla = tuple(elementos)
    tuplas.append(tupla)

  ofertas = [tuple(map(int, elemento[0].split(','))) for elemento in tuplas]
  n = len(ofertas)-1 

  M = int(archivo.readlines()[-1])
  print(M)

  inf = math.inf
  j = int(A/M)
  tabla = [[inf for i in range(j + 1)] for i in range(n+1)]
  solucion = [0] * (n+1)
  optimal = accionesPD2_costo(0, A, ofertas, tabla, M)
  for i in range(n):
    p, c, r = ofertas[i]
    c = int(c/M)
    r = int(r/M)
    for k in range(r, min(j, c) + 1):
      if tabla[i][j] == p * (k * M) + tabla[i + 1][j - k]:
        solucion[i] = k
        j = j - k
        break
  solucion[-1] = j
  salida = str(optimal) + " " + str(solucion)
  return salida