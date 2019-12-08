"""
Instrucciones:
Llamar las funciones en este orden
    problem = main(fileInput)}
    readInput()
    HungarianAssignment()
    
---> main(fileInput) funcion principal que lee un archivo de la matriz con los costos.
--->readInput() almance la matriz
--->HungarianAssignment() ejecuta la resolucion al problema

Repo: https://github.com/isopropylcyanide/Hungarian-Assignment-GUI/blob/master/assignmentProb.py
"""
from itertools import combinations
from collections import deque
from sys import maxsize, argv, exit

_GUI_ROW, _GUI_COL, _GUI_M = 0, 0, None
_backup = None

delimiter = '\n-'
finalResult = None


class HorzLine:
    # Denota una línea horizontal a través de la matriz"

    def __init__(self, pos):
        self.finalResult = None
        self.pos = pos
        self.type = "Horizontal"
        self.across = "row"

    def __repr__(self):
        return 'H%d' % (self.pos)


class VertLine:
    # Denota una línea Vertical a través de la matriz
    def __init__(self, pos):
        self.pos = pos
        self.type = "Vertical"
        self.across = "column"

    def __repr__(self):
        return 'V%d' % (self.pos)


class HungarianAssignment:
    # Una clase que resuelve el problema de asignación húngaro

    def __init__(self):
        self.row, self.col, self.M = 0, 0, None
        self.Z = None

    def printMatrix(self):

        for i in self.M:
            print(i)
            #for j in i:
                #print (' ', j, ' ',)

        print (delimiter)

    def reduceMatrix(self):
    #Devuelve una matriz reducida de fila y columna
        for i in range(self.row):
            minElem = min(self.M[i])
            self.M[i] = list(map(lambda x: x - minElem, self.M[i]))

        # Ahora para cada columna
        for col in range(self.row):
            l = []
            for row in range(self.row):
                l.append(self.M[row][col])
            minElem = min(l)
            for row in range(self.row):
                self.M[row][col] -= minElem

    def getZeroPositions(self):
        """Regresa la posicion actual de los 0's"""
        self.Z = set()
        for i in range(self.row):
            for j in range(self.row):
                if self.M[i][j] == 0:
                    self.Z.add((i, j))

    def printZeroLocations(self):
        print ('\n Zeros are located at follows:\n\n',)
        for i in self.Z:
            print (i)
        print (delimiter)

    def checkAssignments(self):
        #asignación para cubrir los 0's
        global _backup

        bestComb = self.getSetOfCrossingLines()
        len_BC = len(bestComb)
        print ('\n Current best combination covering all zeros: %d\n' % (len_BC))
        for i in bestComb:
            print ('\t%s line through %s : %d\n' % (i.type, i.across, i.pos))
        print (delimiter)

        curAssignments, totalVal = self.getAssignment(), 0
        print ('\n  The assignments are as follows: \n\n',)
        for i in curAssignments:
            x, y = i[0], i[1]
            print ('\t At: ', x, y, ' Value: ',  _backup[x][y], '\n')
            totalVal += _backup[x][y]

        if len(bestComb) != self.row:
            # Verificación
            print ('\n Current solution isn\'t optimal: lines are not enough\n')
            print (delimiter)
            self.tickRowsAndColumns(curAssignments)

        else:
            self.finalResult = '\n  Optimal assignments are as follows: \n\n'
            print ('\n Current solution is optimal: Minimal cost: ', totalVal)
            print (delimiter)
            print ('\n  Final assignments are as follows: \n\n',)
            for i in curAssignments:
                x, y = i[0], i[1]
                print ('\t At: ', x, y, ' Value: ',  _backup[x][y], '\n')
                self.finalResult += '\t At: %d %d \tValue: %d\n\n' % (
                    x, y, _backup[x][y])
            self.finalResult += '\n Minimum cost incurred: %d \n' % (totalVal)
            return

    def getDummy(self, n, m):
        """Agregue una variable ficticia cuando filas! = Columnas"""
        _m = max(n, m)
        print (self.M)
        for i in range(_m):
            for j in range(_m):
                self.M[i][j] = 0 if self.M[i][j] == -1 else self.M[i][j]
        return self.M

    def getSetOfCrossingLines(self):
        #Devuelve un conjunto de líneas que cubren mínimamente todos los ceros
        horzLines = [HorzLine(i) for i in range(self.row)]
        vertLines = [VertLine(i) for i in range(self.row)]
        # Tenemos que elegir n líneas máximas para tachar todos los ceros
        # La asignación es óptima cuando las líneas mínimas son del orden de lamatriz
        allComb, bestComb = [], []
        for i in range(1, self.row + 1):
            allComb.extend(combinations(horzLines + vertLines, i))

        # Encuentra la combinación que cubre las listas en las líneas mínimas
        for i in allComb:
            covered = set()
            for j in i:
                for zero in self.Z:
                    if zero in covered:
                        continue
                    elif j.type == 'Horizontal' and j.pos == zero[0]:
                        covered.add(zero)
                    elif j.type == 'Vertical' and j.pos == zero[1]:
                        covered.add(zero)
            if len(covered) == len(self.Z):
                if bestComb == []:
                    bestComb = i
                elif len(i) < len(bestComb):
                    bestComb = i

        return bestComb

    def getAssignment(self):
        #Asignar el número máximo de 0's posible
        removedSet = set()

        # puede haber n 0's
        bestAssign = set()

        # hay al menos 4 ceros en nuestros n 0's, 
        for comb in combinations(self.Z, self.row):
            removedSet = set()
            totalSet = set(comb)
            curAssign = set()
            for j in totalSet:
                if j in removedSet:
                    continue
                r, c = j[0], j[1]
                # eliminar otros tiene la misma fila / col
                curAssign.add(j)
                for k in totalSet:
                    if k != j and k not in removedSet:
                        if k[0] == r or k[1] == c:
                            removedSet.add(k)
            if len(curAssign) > len(bestAssign):
                bestAssign = curAssign.copy()
        return bestAssign

    def tickRowsAndColumns(self, assignments):
        """
        Marque las filas y columnas en la Matrix consecutivamente:
        - Marcar las filas que no tienen una asignación
        - Marcar los cols que tienen 0 en la fila marcada
        - Marcar todas las filas que tienen asignaciones en la columna marcada
        - Repita el procedimiento anterior hasta que no se pueda marcar más

        """
        global _backup
        tickRows, tickCols = set(range(self.row)), set()
        # marcar renglones sin asignación
        for i in assignments:
            curRow = i[0]
            if curRow in tickRows:
                tickRows.remove(curRow)

        queue = deque(tickRows)
        while queue:
            # Marca los cols que tienen 0 en la fila marcada
            queue.popleft()
            for row in tickRows:
                for col in range(self.row):
                    if self.M[row][col] == 0:
                        tickCols.add(col)

            for col in tickCols:
                for assign in assignments:
                    if assign[1] == col and assign[0] not in tickRows:
                        tickRows.add(assign[0])
                        queue.append(assign[0])

        print ('\n Ticked rows:  ', list(tickRows))
        print (' Ticked cols:  ', list(tickCols))

        # Dibuja líneas rectas a través de filas sin marcar y columnas marcadas
        horLines = [HorzLine(i) for i in range(self.row) if i not in tickRows]
        verLines = [VertLine(i) for i in range(self.row) if i in tickCols]
        bestComb = horLines + verLines

        print ('\n Marking unmarked rows & marked cols:  ', len(bestComb), '\n')
        for i in bestComb:
            print ('\t%s line through %s : %d' % (i.type, i.across, i.pos))
        print (delimiter)

        if horLines + verLines == self.row:
            print ('\n Current solution is optimal\n')
            curAssignments, totalVal = self.getAssignment(), 0
            print ('\n  The assignments are as follows: \n\n',)
            self.finalResult = '\n Optimal assignments are as follows: \n\n'
            for i in curAssignments:
                x, y = i[0], i[1]
                print ('\t At: ', x, y, ' Value: ',  _backup[x][y], '\n')
                self.finalResult += '\t At: %d %d \tValue: %d\n\n' % (
                    x, y, _backup[x][y])
                totalVal += _backup[x][y]
            self.finalResult += '\n\n Minimum cost incurred: %d\n ' % (
                totalVal)
            print (delimiter)
            return True
        else:
            print ('\n Current solution isn\'t optimal : lines aren\'t enough\n')
            print (' Now going for uncovering elements pass\n\n')
            self.smallestElements(bestComb)
            self.getZeroPositions()
            self.printZeroLocations()
            self.checkAssignments()

    def smallestElements(self, bestComb):
        """
        Examina los elementos sin cubir: seleccione min sin cubrir y reste de todos elementos sin cubrir. 
        Para elementos en la intersección de dos líneas,agregue el elemento min
        """
        H_MASK, V_MASK, I_MASK = "H", "V", "I"
        MASK = [[None for i in range(self.row)] for j in range(self.row)]

        for line in bestComb:
            if line.type == "Horizontal":
                row = line.pos
                for col in range(self.row):
                    if MASK[row][col] is None:
                        MASK[row][col] = H_MASK
                    elif MASK[row][col] == V_MASK:
                        MASK[row][col] = I_MASK

            elif line.type == "Vertical":
                col = line.pos
                for row in range(self.row):
                    if MASK[row][col] is None:
                        MASK[row][col] = V_MASK
                    elif MASK[row][col] == H_MASK:
                        MASK[row][col] = I_MASK

        minElem = maxsize
        for i in range(self.row):
            for j in range(self.row):
                if MASK[i][j] == None:
                    minElem = min(minElem, self.M[i][j])
        # Resta min sin cubrir y suma a los elementos de intersección
        for i in range(self.row):
            for j in range(self.row):
                if MASK[i][j] == None:
                    self.M[i][j] -= minElem
                elif MASK[i][j] == I_MASK:
                    self.M[i][j] += minElem

        print ('\n Uncovered matrix\n',)
        self.printMatrix()


def readInput():
    #Leer la matriz del archivo y devolver un objeto HungarianAssignment 
    solver = HungarianAssignment()

    if len(argv) != 2:
        print ('\n No input file feeded')
        print (' Usage: python assignment.py "name_of_InputFile"')
        return solver

    try:
        inputFile = argv[1]
        f = open(inputFile, "r")
        n, m = map(int, f.readline().strip().split(" "))
        _m = max(n, m)
        M = [[-1 for a in range(_m)]
             for b in range(_m)]  # denotes the matrix
        for ind, i in enumerate(f.readlines()):
            for indj, j in enumerate(map(int, i.strip().split(" "))):
                M[ind][indj] = j

        solver.M = M
        if n != m:
            print ('\n Matrices aren\'t of the same order')
            print (' Adding dummy\n')
            print (delimiter)
            solver.getDummy(n, m)
        else:
            print ('\n No dummy required')
        n = _m
        solver.row, solver.col = n, m

    except Exception as e:
        print ('\n Exception occured: %s Check again' % (e))
    finally:
        return solver


def main(fileHandle=None):
    global _backup, finalResult
    # obtiene matriz del archivo
    solver = fillFromGUI() if _GUI_M else readInput()

    if solver.M is None:
        print (' Error occured during execution\n')
        exit()
    _backup = solver.M[:]
    print ('\n Received Matrix: \n',)
    solver.printMatrix()

    # reducir matriz
    solver.reduceMatrix()
    print ('\n Reduced Matrix: \n',)
    solver.printMatrix()

    # obetener posicion de los cerros de la matriz
    solver.getZeroPositions()
    solver.printZeroLocations()

    # verificar asginaciones
    solver.checkAssignments()
    finalResult = solver.finalResult

if __name__ == '__main__':
    main()


