"""
Instrucciones:
Llamar las funciones en este orden
    problem = gen_matrix(v,c)
    constrain(problem, string)
    obj(problem, string)
    maxz(problem)
    
gen_matrix() roduce una matriz para recibir restricciones y una función objetivo para maximizar o minimizar.
    Toma var (número variable) y cons (número de restricciones) como parámetros.
---> gen_matrix(2,3) crea una matrix del diseño del problema.

---> constrain() restricciones del problema. oma el problema como el primer argumento y una cadena como el segundo. La cadena debe ser ingresado en la forma de 1,2, G, 10 que significa 1 (x1) + 2 (x2) >= 10. Use 'L' para <=.

---> Usar obj() solo después de ingresar todas las restricciones, en la forma de 1,2,0 que significa 1 (x1) +2 (x2) +0
    El término final siempre está reservado para una constante y 0 no se puede omitir.
---> Usar maxz()  para resolver un problema de maximización de LP. Use minz () para resolver un problema de minimización.
Bug *** la función pivot(), subcomponente de maxz() y minz(), tiene un par de errores. Hasta ahora, esto solo ha ocurrido cuando minz es llamada
Repo: https://github.com/jdmoore7/simplex_algorithm/blob/master/simplex.py

"""

import numpy as np

# # genera una matriz vacía con un tamaño adecuado para variables y restricciones.
def gen_matrix(var,cons):
    tab = np.zeros((cons+1, var+cons+2))
    return tab

# comprueba la columna más a la derecha en busca de valores negativos SOBRE LA última fila. Si existen valores negativos, se requiere otro pivote.
def next_round_r(table):
    m = min(table[:-1,-1])
    if m>= 0:
        return False
    else:
        return True

# comprueba que la fila inferior, excluyendo la columna final, tenga valores negativos. Si existen valores negativos, se requiere otro pivote.
def next_round(table):
    lr = len(table[:,0])
    m = min(table[lr-1,:-1])
    if m>=0:
        return False
    else:
        return True

# Similar a la función next_round_r, pero devuelve el índice de fila del elemento negativo en la columna más a la derecha
def find_neg_r(table):
    # lc = numero de columnas, lr = numero de renglones
    lc = len(table[0,:])
    # busca en cada fila (excluyendo la última fila) en la columna final el valor mínimo
    m = min(table[:-1,lc-1])
    if m<=0:
        # n = índice de fila de m 
        n = np.where(table[:-1,lc-1] == m)[0][0]
    else:
        n = None
    return n

#devuelve el índice de columna del elemento negativo en la fila inferior
def find_neg(table):
    lr = len(table[:,0])
    m = min(table[lr-1,:-1])
    if m<=0:
        # n = índice de fila para m
        n = np.where(table[lr-1,:-1] == m)[0][0]
    else:
        n = None
    return n

# localiza el elemento pivote en el tabla para eliminar el elemento negativo de la columna más a la derecha.
def loc_piv_r(table):
        total = []
        # r = índice de fila de negativo entry
        r = find_neg_r(table)
        # encuentra todos los elementos en la fila, r, excluyendo la columna final
        row = table[r,:-1]
        # encuentra el valor mínimo en la fila (excluyendo la última columna)
        m = min(row)
        # c = índice de columna para entrada mínima en fila
        c = np.where(row == m)[0][0]
        # todos los elementos en la columna
        col = table[:-1,c]
        # necesita pasar por esta columna para encontrar la relación positiva más pequeña
        for i, b in zip(col,table[:-1,-1]):
            # No puede ser igual a 0 y b/i debe ser positivo.
            if i**2>0 and b/i>0:
                total.append(b/i)
            else:
                # marcador de posición para elementos que no satisfacen los requisitos anteriores. De lo contrario, nuestro número de índice sería defectuoso.
                total.append(0)
        element = max(total)
        for t in total:
            if t > 0 and t < element:
                element = t
            else:
                continue

        index = total.index(element)
        return [index,c]
# proceso similar, devuelve un elemento de matriz específico para pivotar.
def loc_piv(table):
    if next_round(table):
        total = []
        n = find_neg(table)
        for i,b in zip(table[:-1,n],table[:-1,-1]):
            if i**2>0 and b/i>0:
                total.append(b/i)
            else:
                # marcador de posición para elementos que no satisfacen los requisitos anteriores. De lo contrario, nuestro número de índice sería defectuoso.
                total.append(0)
        element = max(total)
        for t in total:
            if t > 0 and t < element:
                element = t
            else:
                continue

        index = total.index(element)
        return [index,n]

# Toma la entrada de cadena y devuelve una lista de números que se organizarán en la tabla
def convert(eq):
    eq = eq.split(',')
    if 'G' in eq:
        g = eq.index('G')
        del eq[g]
        eq = [float(i)*-1 for i in eq]
        return eq
    if 'L' in eq:
        l = eq.index('L')
        del eq[l]
        eq = [float(i) for i in eq]
        return eq

# La fila final de la tabla en un problema de mínimizacion es lo opuesto a un problema de maximización, por lo que los elementos se multiplican por (-1)
def convert_min(table):
    table[-1,:-2] = [-1*i for i in table[-1,:-2]]
    table[-1,-1] = -1*table[-1,-1]
    return table

# genera x1,x2,...xn para el número variable de variables.
def gen_var(table):
    lc = len(table[0,:])
    lr = len(table[:,0])
    var = lc - lr -1
    v = []
    for i in range(var):
        v.append('x'+str(i+1))
    return v

# pivota la tabla de modo que los elementos negativos se eliminen de la última fila y la última columna
def pivot(row,col,table):
    #numero de renglones
    lr = len(table[:,0])
    # numero de columnas
    lc = len(table[0,:])
    t = np.zeros((lr,lc))
    pr = table[row,:]
    if table[row,col]**2>0: 
        e = 1/table[row,col]
        r = pr*e
        for i in range(len(table[:,col])):
            k = table[i,:]
            c = table[i,col]
            if list(k) == list(pr):
                continue
            else:
                t[i,:] = list(k-r*c)
        t[row,:] = list(r)
        return t
    else:
        print('Cannot pivot on this element.')

# comprueba si hay espacio en la matriz para agregar otra restricción
def add_cons(table):
    lr = len(table[:,0])
    # querer saber SI existen al menos 2 filas de todos los elementos cero
    empty = []
    # iterar a través de cada fila
    for i in range(lr):
        total = 0
        for j in table[i,:]:
            # use el valor al cuadrado para que (-x) y (+ x) no se cancelen mutuamente
            total += j**2
        if total == 0:
            # agregue cero a la lista SOLAMENTE si todos los elementos en una fila son cero
            empty.append(total)
    # Hay al menos 2 filas con todos los elementos cero si lo siguiente es verdadero
    if len(empty)>1:
        return True
    else:
        return False

# agrega una restricción a la matriz
def constrain(table,eq):
    if add_cons(table) == True:
        lc = len(table[0,:])
        lr = len(table[:,0])
        var = lc - lr -1
        # configurar el contador para recorrer en iteración la longitud total de las filas
        j = 0
        while j < lr:
            # iterar por renglon
            row_check = table[j,:]
            # el total será la suma de las entradas en la fila
            total = 0
            # Encuentra la primera fila con las 0 entradas
            for i in row_check:
                total += float(i**2)
            if total == 0:
                # Hemos encontrado la primera fila con todas las entradas cero
                row = row_check
                break
            j +=1

        eq = convert(eq)
        i = 0
        # iterar a través de todos los términos en la función de restricción, excluyendo el último
        while i<len(eq)-1:
            # asignar valores de fila de acuerdo con la ecuación
            row[i] = eq[i]
            i +=1
       
        row[-1] = eq[-1]

        # agregue variable de holgura según la ubicación en la tabla.
        row[var+j] = 1
    else:
        print('Cannot add another constraint.')

# comprueba para determinar si se puede agregar una función objetivo a la matriz
def add_obj(table):
    lr = len(table[:,0])
    # want to know IF exactly one row of all zero elements exist
    empty = []
    # iterar a través de cada fila
    for i in range(lr):
        total = 0
        for j in table[i,:]:
            # use el valor al cuadrado para que (-x) y (+ x) no se cancelen mutuamente
            total += j**2
        if total == 0:
            # agregue cero a la lista SOLAMENTE si todos los elementos en una fila son cero
            empty.append(total)
    # Hay exactamente una fila con todos los elementos cero si lo siguiente es verdadero
    if len(empty)==1:
        return True
    else:
        return False

# agrega la función objetivo a la matriz.
def obj(table,eq):
    if add_obj(table)==True:
        eq = [float(i) for i in eq.split(',')]
        lr = len(table[:,0])
        row = table[lr-1,:]
        i = 0
    # iterar a través de todos los términos en la función de restricción, excluyendo el último
        while i<len(eq)-1:
            # assign row values according to the equation
            row[i] = eq[i]*-1
            i +=1
        row[-2] = 1
        row[-1] = eq[-1]
    else:
        print('You must finish adding constraints before the objective function can be added.')

# resuelve el problema de maximización para una solución óptima, devuelve el diccionario con los apuntadores x1, x2 ... xn y max.
def maxz(table, output='summary'):
    while next_round_r(table)==True:
        table = pivot(loc_piv_r(table)[0],loc_piv_r(table)[1],table)
    while next_round(table)==True:
        table = pivot(loc_piv(table)[0],loc_piv(table)[1],table)

    lc = len(table[0,:])
    lr = len(table[:,0])
    var = lc - lr -1
    i = 0
    val = {}
    for i in range(var):
        col = table[:,i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            val[gen_var(table)[i]] = table[loc,-1]
        else:
            val[gen_var(table)[i]] = 0
    val['max'] = table[-1,-1]
    for k,v in val.items():
        val[k] = round(v,6)
    if output == 'table':
        return table
    else:
        return val

# resuelva el problema de minimización para una solución óptima, devuelve el diccionario con las teclas / x1, x2 ... xn y max.
def minz(table, output='summary'):
    table = convert_min(table)

    while next_round_r(table)==True:
        table = pivot(loc_piv_r(table)[0],loc_piv_r(table)[1],table)
    while next_round(table)==True:
        table = pivot(loc_piv(table)[0],loc_piv(table)[1],table)

    lc = len(table[0,:])
    lr = len(table[:,0])
    var = lc - lr -1
    i = 0
    val = {}
    for i in range(var):
        col = table[:,i]
        s = sum(col)
        m = max(col)
        if float(s) == float(m):
            loc = np.where(col == m)[0][0]
            val[gen_var(table)[i]] = table[loc,-1]
        else:
            val[gen_var(table)[i]] = 0
    val['min'] = table[-1,-1]*-1
    for k,v in val.items():
        val[k] = round(v,6)
    if output == 'table':
        return table
    else:
        return val

if __name__ == "__main__":
    #Problema primal
    m = gen_matrix(17,8)
    constrain(m,'1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,L,1')
    constrain(m,'0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,L,1')
    constrain(m,'0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,L,1')
    constrain(m,'0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,L,1')
    
    constrain(m,'1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,L,1')
    constrain(m,'0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,L,1')
    constrain(m,'0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,L,1')
    constrain(m,'0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,L,1')
    
    obj(      m,'48,48,50,44,56,60,60,68,96,94,90,85,42,44,54,46,0')
    print("primal: ")
    print(maxz(m))
    
    #Problema Dual
    m2= gen_matrix(8,16)
    # col        1 2 3 4 5 6 7 8
    constrain(m2,'1,0,0,0,1,0,0,0,L,48')
    constrain(m2,'1,0,0,0,0,1,0,0,L,48')
    constrain(m2,'1,0,0,0,0,0,1,0,L,50')
    constrain(m2,'1,0,0,0,0,0,0,1,L,44')
    
    constrain(m2,'0,1,0,0,1,0,0,0,L,56')
    constrain(m2,'0,1,0,0,0,1,0,0,L,60')
    constrain(m2,'0,1,0,0,0,0,1,0,L,60')
    constrain(m2,'0,1,0,0,0,0,0,1,L,68')
    
    constrain(m2,'0,0,1,0,1,0,0,0,L,96')
    constrain(m2,'0,0,1,0,0,1,0,0,L,94')
    constrain(m2,'0,0,1,0,0,0,1,0,L,90')
    constrain(m2,'0,0,1,0,0,0,0,1,L,85')
    
    constrain(m2,'0,0,0,1,1,0,0,0,L,42')
    constrain(m2,'0,0,0,1,0,1,0,0,L,44')
    constrain(m2,'0,0,0,1,0,0,1,0,L,54')
    constrain(m2,'0,0,0,1,0,0,0,1,L,46')
    obj(m2,      '1,1,1,1,1,1,1,1,0')
    print('\n')
    print("dual")
    print(maxz(m2))

